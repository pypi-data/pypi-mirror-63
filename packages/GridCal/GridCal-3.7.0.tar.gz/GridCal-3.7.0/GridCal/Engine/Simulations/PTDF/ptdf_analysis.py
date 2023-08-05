# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.
import numpy as np
from typing import List
from enum import Enum

from GridCal.Engine.basic_structures import Logger
from GridCal.Engine.Core.multi_circuit import MultiCircuit
from GridCal.Engine.Core.snapshot_static_inputs import StaticSnapshotInputs, StaticSnapshotIslandInputs
from GridCal.Engine.Simulations.PowerFlow.power_flow_worker import single_island_pf, PowerFlowResults
from GridCal.Engine.Simulations.PowerFlow.power_flow_options import PowerFlowOptions
from GridCal.Engine.Simulations.PTDF.ptdf_results import PTDFVariation


class PtdfGroupMode(Enum):
    ByTechnology = 'By technology'
    ByNode = 'By node'
    ByGenLoad = 'By Generator and Load'


def group_generators_by_technology(circuit: MultiCircuit):
    """
    Compose a dictionary of generator groups
    :param circuit: MultiCircuit
    :return: dictionary [Technology] : [generator indices]
    """
    gens = circuit.get_generators()

    groups = dict()

    for i, gen in enumerate(gens):

        if gen.technology in groups.keys():
            arr = np.r_[groups[gen.technology], i]
            groups[gen.technology] = arr

        else:
            groups[gen.technology] = np.array([i])

    return groups


def get_ptdf_variations(circuit: MultiCircuit, numerical_circuit: StaticSnapshotInputs, group_mode: PtdfGroupMode, power_amount):
    """
    Get the PTDF variations
    :param circuit: MultiCircuit instance
    :param numerical_circuit: NumericalCircuit instance (faster)
    :param group_mode: group generators by technology?
    :param power_amount: power amount to vary. if group_by_technology the variation applies by group otherwise per
                         individual generator
    :return: list of Variations (instances of PTDFVariation)
    """
    variations = list()

    # declare the default variation object and store it
    var = PTDFVariation(name='Default', n=numerical_circuit.nbus, original_power=power_amount)
    variations.append(var)

    # compute the per unit power
    power = power_amount / circuit.Sbase

    if group_mode == PtdfGroupMode.ByTechnology:

        # get generator groups by technology
        groups = group_generators_by_technology(circuit=circuit)

        for key, indices in groups.items():
            ng = len(indices)

            # power increment by technology of all the generators
            dPg = np.ones(ng) * power / float(ng)

            # declare the variation object
            var = PTDFVariation(name=key, n=numerical_circuit.nbus, original_power=power_amount)

            # power increment by bus
            var.dP = numerical_circuit.C_bus_gen[:, indices] * dPg

            # store the variation
            variations.append(var)

    elif group_mode == PtdfGroupMode.ByGenLoad:

        # add the generation variations
        for i in range(numerical_circuit.n_ctrl_gen):

            # generate array of zeros, and modify the generation for the particular generator
            dPg = np.zeros(numerical_circuit.n_ctrl_gen)
            dPg[i] = power

            # declare the variation object
            var = PTDFVariation(name=numerical_circuit.generator_names[i],
                                n=numerical_circuit.nbus,
                                original_power=power_amount)

            # power increment by bus
            var.dP = numerical_circuit.C_bus_gen * dPg

            # store the variation
            variations.append(var)

        # add the load variations
        for i in range(numerical_circuit.n_ld):

            # generate array of zeros, and modify the generation for the particular generator
            dPg = np.zeros(numerical_circuit.n_ld)
            dPg[i] = -power

            # declare the variation object
            var = PTDFVariation(name=numerical_circuit.load_names[i],
                                n=numerical_circuit.nbus,
                                original_power=power_amount)

            # power increment by bus
            var.dP = numerical_circuit.C_bus_load * dPg

            # store the variation
            variations.append(var)

    elif group_mode == PtdfGroupMode.ByNode:

        # add the generation variations
        for i in range(numerical_circuit.nbus):

            # declare the variation object
            var = PTDFVariation(name=numerical_circuit.bus_names[i],
                                n=numerical_circuit.nbus,
                                original_power=power_amount)

            # generate array of zeros, and modify the generation for the particular generator
            var.dP = np.zeros(numerical_circuit.nbus)
            var.dP[i] = power

            # store the variation
            variations.append(var)

    else:
        raise Exception('PTDF grouping mode not implemented: ' + str(group_mode))

    return variations


def power_flow_worker(variation: int, nbus, nbr, calculation_inputs: List[StaticSnapshotIslandInputs],
                      options: PowerFlowOptions, dP, return_dict):
    """
    Run asynchronous power flow
    :param variation: variation id
    :param nbus: number of buses
    :param nbr: number of branches
    :param calculation_inputs: list of CalculationInputs' instances
    :param options: PowerFlowOptions instance
    :param dP: delta of active power (array of values of size nbus)
    :param return_dict: dictionary to return values
    :return: Nothing because it is a worker, the return is done via the return_dict variable
    """
    # create new results
    pf_results = PowerFlowResults()
    pf_results.initialize(nbus, nbr)
    logger = Logger()

    # simulate each island and merge the results
    for i, calculation_input in enumerate(calculation_inputs):

        if len(calculation_input.ref) > 0:

            # run circuit power flow
            res = single_island_pf(circuit=calculation_input,
                                   Vbus=calculation_input.Vbus,
                                   Sbus=calculation_input.Sbus - dP[calculation_input.original_bus_idx],
                                   Ibus=calculation_input.Ibus,
                                   branch_rates=calculation_input.branch_rates,
                                   options=options,
                                   logger=Logger())

            bus_original_idx = calculation_input.original_bus_idx
            branch_original_idx = calculation_input.original_branch_idx

            # merge the results from this island
            pf_results.apply_from_island(res, bus_original_idx, branch_original_idx)

        else:
            logger.append('There are no slack nodes in the island ' + str(i))

    return_dict[variation] = (pf_results, logger)





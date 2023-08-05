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
from matplotlib import pyplot as plt
from PySide2.QtCore import QThread, Signal

from GridCal.Engine.basic_structures import Logger
from GridCal.Engine.Simulations.PowerFlow.power_flow_options import PowerFlowOptions
from GridCal.Gui.GuiFunctions import ResultsModel
from GridCal.Engine.Simulations.result_types import ResultTypes
from GridCal.Engine.Core.multi_circuit import MultiCircuit
from GridCal.Engine.Simulations.PowerFlow.helm_power_flow import helm_coefficients_josep, sigma_function


class SigmaAnalysisResults:

    def __init__(self, n):

        self.n = n

        self.name = 'Power flow'

        self.lambda_value = 1.0

        self.Sbus = np.zeros(n, dtype=complex)

        self.distances = np.zeros(n, dtype=float)

        self.sigma_re = np.zeros(n, dtype=float)

        self.sigma_im = np.zeros(n, dtype=float)

        self.available_results = [ResultTypes.SigmaReal,
                                  ResultTypes.SigmaImag,
                                  ResultTypes.SigmaDistances,
                                  ResultTypes.SigmaPlusDistances]

        self.elapsed = 0

        self.convergence_reports = list()

    def apply_from_island(self, results: "SigmaAnalysisResults", b_idx):
        """
        Apply results from another island circuit to the circuit results represented
        here.

        Arguments:

            **results**: PowerFlowResults

            **b_idx**: bus original indices

            **br_idx**: branch original indices
        """
        self.Sbus[b_idx] = results.Sbus

        self.distances[b_idx] = results.distances

        self.sigma_re[b_idx] = results.sigma_re

        self.sigma_im[b_idx] = results.sigma_im

    def plot(self, ax, npoints=1000):
        """
        Plot the analysis
        :param ax:
        :param npoints:
        :return:
        """
        if ax is None:
            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111)

        sx = np.linspace(-0.25, np.max(self.sigma_re) + 0.1, npoints)
        sy1 = np.sqrt(0.25 + sx)
        sy2 = -np.sqrt(0.25 + sx)

        ax.plot(sx, sy1, 'k', linewidth=2)
        ax.plot(sx, sy2, 'k', linewidth=2)
        ax.plot(self.sigma_re, self.sigma_im, 'o')
        ax.set_title('Sigma plot')
        ax.set_xlabel('$\sigma_{re}$')
        ax.set_ylabel('$\sigma_{im}$')

    def mdl(self, result_type: ResultTypes, indices=None, names=None) -> "ResultsModel":
        """

        :param result_type:
        :param ax:
        :param indices:
        :param names:
        :return:
        """

        if indices is None and names is not None:
            indices = np.array(range(len(names)))

        if len(indices) > 0:
            labels = names[indices]

            if result_type == ResultTypes.SigmaDistances:
                y = np.abs(self.distances[indices])
                y_label = '(p.u.)'
                title = 'Sigma distances '

            elif result_type == ResultTypes.SigmaReal:
                y = self.sigma_re[indices]
                y_label = '(deg)'
                title = 'Real sigma '

            elif result_type == ResultTypes.SigmaImag:
                y = self.sigma_im[indices]
                y_label = '(p.u.)'
                title = 'Imaginary Sigma '

            elif result_type == ResultTypes.SigmaPlusDistances:
                y = np.c_[self.sigma_re[indices], self.sigma_im[indices], self.distances[indices]]
                y_label = '(p.u.)'
                title = 'Sigma and distances'

                mdl = ResultsModel(data=y, index=labels, columns=['σ real', 'σ imaginary', 'Distances'],
                                   title=title, ylabel=y_label, units=y_label)
                return mdl

            else:
                n = len(labels)
                y = np.zeros(n)
                y_label = ''
                title = ''

            # assemble model
            mdl = ResultsModel(data=y, index=labels, columns=[result_type.value[0]],
                               title=title, ylabel=y_label, units=y_label)
            return mdl

        else:
            return None


def multi_island_sigma(multi_circuit: MultiCircuit, options: PowerFlowOptions, logger=Logger()) -> "SigmaAnalysisResults":
    """
    Multiple islands power flow (this is the most generic power flow function)
    :param multi_circuit: MultiCircuit instance
    :param options: PowerFlowOptions instance
    :param logger: list of events to add to
    :return: PowerFlowResults instance
    """
    # print('PowerFlowDriver at ', self.grid.name)
    n = len(multi_circuit.buses)
    m = len(multi_circuit.branches)
    results = SigmaAnalysisResults(n)

    numerical_circuit = multi_circuit.compile_snapshot()

    calculation_inputs = numerical_circuit.compute(apply_temperature=options.apply_temperature_correction,
                                                   branch_tolerance_mode=options.branch_impedance_tolerance_mode,
                                                   ignore_single_node_islands=options.ignore_single_node_islands)

    if len(calculation_inputs) > 1:

        # simulate each island and merge the results
        for i, calculation_input in enumerate(calculation_inputs):

            if len(calculation_input.ref) > 0:
                # V, converged, norm_f, Scalc, iter_, elapsed, Sig_re, Sig_im
                U, X, Q, iter_ = helm_coefficients_josep(Yseries=calculation_input.Yseries,
                                                         V0=calculation_input.Vbus,
                                                         S0=calculation_input.Sbus,
                                                         Ysh0=calculation_input.Ysh,
                                                         pq=calculation_input.pq,
                                                         pv=calculation_input.pv,
                                                         sl=calculation_input.ref,
                                                         pqpv=calculation_input.pqpv,
                                                         tolerance=options.tolerance,
                                                         max_coeff=options.max_iter,
                                                         verbose=False,)

                # compute the sigma values
                n = calculation_input.nbus
                Sig_re = np.zeros(n, dtype=float)
                Sig_im = np.zeros(n, dtype=float)
                Sigma = sigma_function(U, X, iter_ - 1, calculation_input.Vbus[calculation_input.ref])
                Sig_re[calculation_input.pqpv] = np.real(Sigma)
                Sig_im[calculation_input.pqpv] = np.imag(Sigma)
                sigma_distances = np.abs(sigma_distance(Sig_re, Sig_im))

                # store the results
                island_results = SigmaAnalysisResults(n=len(calculation_input.Vbus))
                island_results.lambda_value = 1.0
                island_results.Sbus = calculation_input.Sbus
                island_results.sigma_re = Sig_re
                island_results.sigma_im = Sig_im
                island_results.distances = sigma_distances

                bus_original_idx = calculation_input.original_bus_idx

                # merge the results from this island
                results.apply_from_island(island_results, bus_original_idx)

            else:
                logger.append('There are no slack nodes in the island ' + str(i))
    else:

        if len(calculation_inputs[0].ref) > 0:
            # only one island
            calculation_input = calculation_inputs[0]

            U, X, Q, iter_ = helm_coefficients_josep(Yseries=calculation_input.Yseries,
                                                     V0=calculation_input.Vbus,
                                                     S0=calculation_input.Sbus,
                                                     Ysh0=calculation_input.Ysh,
                                                     pq=calculation_input.pq,
                                                     pv=calculation_input.pv,
                                                     sl=calculation_input.ref,
                                                     pqpv=calculation_input.pqpv,
                                                     tolerance=options.tolerance,
                                                     max_coeff=options.max_iter,
                                                     verbose=False, )

            # compute the sigma values
            n = calculation_input.nbus
            Sig_re = np.zeros(n, dtype=float)
            Sig_im = np.zeros(n, dtype=float)
            Sigma = sigma_function(U, X, iter_ - 1, calculation_input.Vbus[calculation_input.ref])
            Sig_re[calculation_input.pqpv] = np.real(Sigma)
            Sig_im[calculation_input.pqpv] = np.imag(Sigma)
            sigma_distances = np.abs(sigma_distance(Sig_re, Sig_im))

            # store the results
            results = SigmaAnalysisResults(n=len(calculation_input.Vbus))
            results.lambda_value = 1.0
            results.Sbus = calculation_input.Sbus
            results.sigma_re = Sig_re
            results.sigma_im = Sig_im
            results.distances = sigma_distances
        else:
            logger.append('There are no slack nodes')

    return results


def sigma_distance(a, b):
    """
    Distance to the collapse in the sigma space

    The boundary curve is given by y = sqrt(1/4 + x)

    the distance is d = sqrt((x-a)^2 + (sqrt(1/4+ x) - b)^2)

    the derivative of this is d'=(2 (-a + x) + (-b + sqrt(1/4 + x))/sqrt(1/4 + x))/(2 sqrt((-a + x)^2 + (-b + sqrt(1/4 + x))^2))

    Making d'=0, and solving for x, we obtain:

    x1 = 1/12 (-64 a^3 + 48 a^2 + 12 sqrt(3) sqrt(-64 a^3 b^2 + 48 a^2 b^2 - 12 a b^2 + 108 b^4 + b^2) - 12 a + 216 b^2 + 1)^(1/3) - (-256 a^2 + 128 a - 16)/
         (192 (-64 a^3 + 48 a^2 + 12 sqrt(3) sqrt(-64 a^3 b^2 + 48 a^2 b^2 - 12 a b^2 + 108 b^4 + b^2) - 12 a + 216 b^2 + 1)^(1/3)) + 1/12 (8 a - 5)

    x2 = 1/12 (-64 a^3 + 48 a^2 + 12 sqrt(3) sqrt(-64 a^3 b^2 + 48 a^2 b^2 - 12 a b^2 + 108 b^4 + b^2) - 12 a + 216 b^2 + 1)^(1/3) - (-256 a^2 + 128 a - 16)/
         (192 (-64 a^3 + 48 a^2 + 12 sqrt(3) sqrt(-64 a^3 b^2 + 48 a^2 b^2 - 12 a b^2 + 108 b^4 + b^2) - 12 a + 216 b^2 + 1)^(1/3)) + 1/12 (8 a - 5)
    :param a: Sigma real
    :param b: Sigma imag
    :return: distance of the sigma point to the curve sqrt(0.25 + x)
    """

    t1 = (-64 * a**3
          + 48 * a**2
          + 12 * np.sqrt(3)*np.sqrt(-64 * a**3 * b**2
                                    + 48 * a**2 * b**2
                                    - 12 * a * b**2
                                    + 108 * b**4 + b**2)
          - 12 * a + 216 * b**2 + 1)**(1 / 3)

    x1 = 1 / 12 * t1 - (-256 * a**2 + 128*a - 16) / (192 * t1) + 1 / 12 * (8 * a - 5)
    return x1


class SigmaAnalysisDriver(QThread):
    progress_signal = Signal(float)
    progress_text = Signal(str)
    done_signal = Signal()
    name = 'Sigma Analysis'

    def __init__(self, grid: MultiCircuit, options: PowerFlowOptions):
        """
        PowerFlowDriver class constructor
        :param grid: MultiCircuit instance
        :param options: PowerFlowOptions instance
        """

        QThread.__init__(self)

        # Grid to run a power flow in
        self.grid = grid

        # Options to use
        self.options = options

        self.results = None

        self.logger = Logger()

        self.convergence_reports = list()

        self.__cancel__ = False

    @staticmethod
    def get_steps():
        """

        :return:
        """
        return list()

    def run(self):
        """
        Pack run_pf for the QThread
        :return:
        """
        self.results = multi_island_sigma(multi_circuit=self.grid,
                                          options=self.options,
                                          logger=self.logger)

        # send the finnish signal
        self.progress_signal.emit(0.0)
        self.progress_text.emit('Done!')
        self.done_signal.emit()

    def cancel(self):
        self.__cancel__ = True


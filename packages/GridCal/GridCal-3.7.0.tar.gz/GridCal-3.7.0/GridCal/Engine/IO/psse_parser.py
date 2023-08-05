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

import chardet
import re
from typing import List, AnyStr

from GridCal.Engine.basic_structures import Logger
from GridCal.Engine.Core.multi_circuit import MultiCircuit
from GridCal.Engine.Devices import *


class PSSeGrid:

    def __init__(self, data):
        """
        IC
            New Case Flag:
            0 for base case input (i.e., clear the working case before adding data to it)
            1 to add data to the working case
            IC = 0 by default.
        SBASE System MVA base. SBASE = 100.0 by default.
        REV = current revision (32) by default.
        XFRRAT Units of transformer ratings (refer to Transformer Data). The transformer percent
            loading units program option setting (refer to Saved Case Specific Option Settings) is
            set according to this data value.
            XFRRAT < 0 for MVA
            XFRRAT > 0 for current expressed as MVA
            XFRRAT = present transformer percent loading program option setting by default
            (refer to activity OPTN).
        NXFRAT
            Units of ratings of non-transformer branches (refer to Non-Transformer Branch
            Data ). The non-transformer branch percent loading units program option setting
            (refer to Saved Case Specific Option Settings) is set according to this data value.
            NXFRAT < 0 for MVA
            NXFRAT > 0 for current expressed as MVA
            NXFRAT = present non-transformer branch percent loading program option setting
            by default (refer to activity OPTN).
        BASFRQ
            System base frequency in Hertz. The base frequency program option setting (refer to
            Saved Case Specific Option Settings) is set to this data value. BASFRQ = present
            base frequency program option setting value by default (refer to activity OPTN).
        Args:
            data: array with the values
        """

        self.IC, self.SBASE, self.REV, self.XFRRAT, self.NXFRAT, self.BASFRQ = data

        """
        Case Identification Data
        Bus Data
        Load Data
        Fixed Bus Shunt Data
        Generator Data
        Non-Transformer Branch Data
        Transformer Data
        Area Interchange Data
        Two-Terminal DC Transmission Line Data
        Voltage Source Converter (VSC) DC Transmission Line Data
        Transformer Impedance Correction Tables
        Multi-Terminal DC Transmission Line Data
        Multi-Section Line Grouping Data
        Zone Data
        Interarea Transfer Data
        Owner Data
        FACTS Device Data
        Switched Shunt Data
        GNE Device Data
        Induction Machine Data
        Q Record
        """
        self.buses = list()
        self.loads = list()
        self.shunts = list()
        self.switched_shunts = list()
        self.generators = list()
        self.branches = list()
        self.transformers = list()
        self.areas = list()
        self.zones = list()

    def get_circuit(self, logger: Logger):
        """
        Return GridCal circuit
        Returns:

        """

        circuit = MultiCircuit()
        circuit.Sbase = self.SBASE

        area_dict = {elm.I: elm.ARNAME for elm in self.areas}

        zones_dict = {elm.I: elm.ZONAME for elm in self.zones}

        # ---------------------------------------------------------------------
        # Bus related
        # ---------------------------------------------------------------------
        psse_bus_dict = dict()
        for psse_bus in self.buses:

            # relate each PSS bus index with a GridCal bus object
            psse_bus_dict[psse_bus.I] = psse_bus.bus

            # replace area idx by area name if available
            if abs(psse_bus.bus.area) in area_dict.keys():
                psse_bus.bus.area = area_dict[abs(psse_bus.bus.area)]

            if abs(psse_bus.bus.zone) in zones_dict.keys():
                psse_bus.bus.zone = zones_dict[abs(psse_bus.bus.zone)]

            # add the bus to the circuit
            circuit.add_bus(psse_bus.bus)

        # Go through loads
        for psse_load in self.loads:

            bus = psse_bus_dict[psse_load.I]
            api_obj = psse_load.get_object(bus, logger)

            circuit.add_load(bus, api_obj)

        # Go through shunts
        for psse_shunt in self.shunts + self.switched_shunts:

            bus = psse_bus_dict[psse_shunt.I]
            api_obj = psse_shunt.get_object(bus, logger)

            circuit.add_shunt(bus, api_obj)

        # Go through generators
        for psse_gen in self.generators:

            bus = psse_bus_dict[psse_gen.I]
            api_obj = psse_gen.get_object(logger)

            circuit.add_generator(bus, api_obj)

        # ---------------------------------------------------------------------
        # Branches
        # ---------------------------------------------------------------------
        # Go through Branches
        for psse_banch in self.branches:
            # get the object
            branch = psse_banch.get_object(psse_bus_dict, self.SBASE, logger)

            # Add to the circuit
            circuit.add_branch(branch)

        # Go through Transformers
        for psse_banch in self.transformers:
            # get the object
            branches = psse_banch.get_object(psse_bus_dict, logger)

            # Add to the circuit
            for branch in branches:
                circuit.add_branch(branch)

        return circuit


class PSSeBus:

    def __init__(self, data, version, logger: list):
        """
        I: Bus number (1 through 999997). No default allowed.
        NAME Alphanumeric identifier assigned to bus I. NAME may be up to twelve characters
            and may contain any combination of blanks, uppercase letters, numbers and
            special characters, but the first character must not be a minus sign. NAME must
            be enclosed in single or double quotes if it contains any blanks or special char-
            acters. NAME is twelve blanks by default.
        BASKV: Bus base voltage; entered in kV. BASKV = 0.0 by default.
        IDE: Bus type code:
            1 -> for a load bus or passive node (no generator boundary condition) 
            2 -> for a generator or plant bus (either voltage regulating or fixed Mvar) 
            3 -> for a swing bus 
            4 -> for a disconnected (isolated) bus
            IDE = 1 by default.
        AREA: Area number (1 through 9999). AREA = 1 by default.
        ZONE: Zone number (1 through 9999). ZONE = 1 by default.
        OWNER: Owner number (1 through 9999). OWNER = 1 by default.
        VM: Bus voltage magnitude; entered in pu. VM = 1.0 by default.
        VA: Bus voltage phase angle; entered in degrees. VA = 0.0 by default.
        NVHI: Normal voltage magnitude high limit; entered in pu. NVHI=1.1 by default
        NVLO: Normal voltage magnitude low limit, entered in pu. NVLO=0.9 by default
        EVHI: Emergency voltage magnitude high limit; entered in pu. EVHI=1.1 by default
        EVLO: Emergency voltage magnitude low limit; entered in pu. EVLO=0.9 by default
        Args:
            data:
        """

        bustype = {1: BusMode.PQ, 2: BusMode.PV, 3: BusMode.REF, 4: BusMode.PQ}

        if version == 33:
            n = len(data[0])
            dta = np.zeros(13, dtype=object)
            dta[0:n] = data[0]

            self.I, self.NAME, self.BASKV, self.IDE, self.AREA, self.ZONE, \
             self.OWNER, self.VM, self.VA, self.NVHI, self.NVLO, self.EVHI, self.EVLO = dta

            # create bus
            name = self.NAME
            self.bus = Bus(name=name, vnom=self.BASKV, vmin=self.EVLO, vmax=self.EVHI, xpos=0, ypos=0, active=True,
                           area=self.AREA, zone=self.ZONE)

        elif version == 32:

            self.I, self.NAME, self.BASKV, self.IDE, self.AREA, self.ZONE, self.OWNER, self.VM, self.VA = data[0]

            # create bus
            name = self.NAME
            self.bus = Bus(name=name, vnom=self.BASKV, vmin=0.9, vmax=1.1, xpos=0, ypos=0,
                           active=True, area=self.AREA, zone=self.ZONE)

        elif version in [29, 30]:
            # I, ’NAME’, BASKV, IDE, GL, BL, AREA, ZONE, VM, VA, OWNER
            self.I, self.NAME, self.BASKV, self.IDE, self.GL, self.BL, \
             self.AREA, self.ZONE, self.VM, self.VA, self.OWNER = data[0]

            # create bus
            name = self.NAME
            self.bus = Bus(name=name, vnom=self.BASKV, vmin=0.9, vmax=1.1, xpos=0, ypos=0,
                           active=True, area=self.AREA, zone=self.ZONE)

            if self.GL > 0 or self.BL > 0:
                sh = Shunt(name='Shunt_' + str(self.I),
                           G=self.GL, B=self.BL,
                           active=True)

                self.bus.shunts.append(sh)

        else:
            logger.append('Bus not implemented for version ' + str(version))

        # set type
        if self.IDE in bustype.keys():
            self.bus.type = bustype[self.IDE]
        else:
            self.bus.type = BusMode.PQ

        if int(self.IDE) == 4:
            self.bus.active = False

        if self.bus.type == BusMode.REF:
            self.bus.is_slack = True

        if int(self.IDE) == 4:
            self.bus.active = False

        # Ensures unique name
        self.bus.name = str(self.I) + '_' + self.bus.name.replace("'", "").strip()


class PSSeLoad:

    def __init__(self, data, version, logger: list):
        """
        I: Bus number, or extended bus name enclosed in single quotes (refer to Extended Bus
            Names). No default allowed.
        ID: One- or two-character uppercase non-blank alphanumeric load identifier used to
            distinguish among multiple loads at bus I. It is recommended that, at buses for which
            a single load is present, the load be designated as having the load identifier 1. ID = 1
            by default.
        STATUS: Load status of one for in-service and zero for out-of-service. STATUS = 1 by default.
        AREA: Area to which the load is assigned (1 through 9999). By default, AREA is the area to
            which bus I is assigned (refer to Bus Data).
        ZONE: Zone to which the load is assigned (1 through 9999). By default, ZONE is the zone to
            which bus I is assigned (refer to Bus Data).
        PL: Active power component of constant MVA load; entered in MW. PL = 0.0 by default.
        QL: Reactive power component of constant MVA load; entered in Mvar. QL = 0.0 by
            default.
        IP: Active power component of constant current load; entered in MW at one per unit
            voltage. IP = 0.0 by default.
        IQ: Reactive power component of constant current load; entered in Mvar at one per unit
            voltage. IQ = 0.0 by default.
        YP: Active power component of constant admittance load; entered in MW at one per unit
            voltage. YP = 0.0 by default.
        YQ: Reactive power component of constant admittance load; entered in Mvar at one per
            unit voltage. YQ is a negative quantity for an inductive load and positive for a capacitive load.
            YQ = 0.0 by default.
        OWNER: Owner to which the load is assigned (1 through 9999). By default, OWNER is the
            owner to which bus I is assigned (refer to Bus Data).
        SCALE: Load scaling flag of one for a scalable load and zero for a fixed load (refer to SCAL).
            SCALE = 1 by default.
        INTRPT: Interruptible load flag of one for an interruptible load for zero for a non interruptible
            load. INTRPT=0 by default.
        Args:
            data:
        """

        if version == 33:

            n = len(data[0])
            dta = np.zeros(14, dtype=object)
            dta[0:n] = data[0]

            self.I, self.ID, self.STATUS, self.AREA, self.ZONE, self.PL, self.QL, \
             self.IP, self.IQ, self.YP, self.YQ, self.OWNER, self.SCALE, self.INTRPT = dta

        elif version == 32:

            self.I, self.ID, self.STATUS, self.AREA, self.ZONE, self.PL, self.QL, \
             self.IP, self.IQ, self.YP, self.YQ, self.OWNER, self.SCALE = data[0]

        elif version in [29, 30]:
            # I, ID, STATUS, AREA, ZONE, PL, QL, IP, IQ, YP, YQ, OWNER
            self.I, self.ID, self.STATUS, self.AREA, self.ZONE, \
             self.PL, self.QL, self.IP, self.IQ, self.YP, self.YQ, self.OWNER = data[0]

        else:
            logger.append('Load not implemented for version ' + str(version))

    def get_object(self, bus: Bus, logger: list):
        """
        Return GridCal Load object
        Returns:
            Gridcal Load object
        """

        # GL and BL come in MW and MVAr
        vv = bus.Vnom ** 2.0

        if vv == 0:
            logger.append('Voltage equal to zero in shunt conversion!!!')

        g, b = self.YP, self.YQ
        ir, ii = self.IP, self.IQ
        p, q = self.PL, self.QL
        name = str(self.I) + '_' + self.ID.replace("'", "")
        elm = Load(name=name,
                   active=bool(self.STATUS),
                   G=g, B=b,
                   Ir=ir, Ii=ii,
                   P=p, Q=q)

        return elm


class PSSeSwitchedShunt:

    def __init__(self, data, version, logger: list):
        """
        I Bus number, or extended bus name enclosed in single quotes (refer to Extended
            Bus Names). No default allowed.
        MODSW Control mode:
            0 locked
            1 discrete adjustment, controlling voltage locally or at bus SWREM
            2 continuous adjustment, controlling voltage locally or at bus SWREM
            3 discrete adjustment, controlling the reactive power output of the
              plant at bus SWREM
            4 discrete adjustment, controlling the reactive power output of
              the VSC dc line converter at bus SWREM of the VSC dc line
              for which the name is specified as RMIDNT
            5 discrete adjustment, controlling the admittance setting of the
              switched shunt at bus SWREM
            6 discrete adjustment, controlling the reactive power output of the
              shunt element of the FACTS device for which the name is specified
              as RMIDNT
              MODSW = 1 by default.
        ADJM Adjustment method:
            0 steps and blocks are switched on in input order, and off in reverse
             input order; this adjustment method was the only method available
             prior to PSS®E-32.0.
            1 steps and blocks are switched on and off such that the next highest
             (or lowest, as appropriate) total admittance is achieved.
            ADJM = 0 by default.
        STAT Initial switched shunt status of one for in-service and zero for out-of-service;
            STAT = 1 by default.
        VSWHI When MODSW is 1 or 2, the controlled voltage upper limit; entered in pu.
            When MODSW is 3, 4, 5 or 6, the controlled reactive power range upper limit;
            entered in pu of the total reactive power range of the controlled voltage controlling
            device.
            VSWHI is not used when MODSW is 0. VSWHI = 1.0 by default
        VSWLO When MODSW is 1 or 2, the controlled voltage lower limit; entered in pu.
            When MODSW is 3, 4, 5 or 6, the controlled reactive power range lower limit;
            entered in pu of the total reactive power range of the controlled voltage controlling
            device.
            VSWLO is not used when MODSW is 0. VSWLO = 1.0 by default.
        SWREM Bus number, or extended bus name enclosed in single quotes (refer to Extended
            Bus Names), of the bus where voltage or connected equipment reactive power
            output is controlled by this switched shunt.
            When MODSW is 1 or 2, SWREM is entered as 0 if the switched shunt is to regulate
            its own voltage; otherwise, SWREM specifies the remote Type 1 or 2 bus where
            voltage is to be regulated by this switched shunt
            When MODSW is 3, SWREM specifies the Type 2 or 3 bus where plant reactive
            power output is to be regulated by this switched shunt. Set SWREM to I if the
            switched shunt and the plant that it controls are connected to the same bus.
            When MODSW is 4, SWREM specifies the converter bus of a VSC dc line where
            converter reactive power output is to be regulated by this switched shunt. Set
            SWREM to I if the switched shunt and the VSC dc line converter that it controls are
            connected to the same bus.
            When MODSW is 5, SWREM specifies the remote bus to which the switched shunt
            for which the admittance setting is to be regulated by this switched shunt is
            connected.
            SWREM is not used when MODSW is 0 or 6. SWREM = 0 by default.
        RMPCT Percent of the total Mvar required to hold the voltage at the bus controlled by bus I
            that are to be contributed by this switched shunt; RMPCT must be positive. RMPCT
            is needed only if SWREM specifies a valid remote bus and there is more than one
            local or remote voltage controlling device (plant, switched shunt, FACTS device
            shunt element, or VSC dc line converter) controlling the voltage at bus SWREM to a
            setpoint, or SWREM is zero but bus I is the controlled bus, local or remote, of one or
            more other setpoint mode voltage controlling devices. Only used if MODSW = 1 or
            2. RMPCT = 100.0 by default.
        RMIDNT When MODSW is 4, the name of the VSC dc line where the converter bus is specified in SWREM.
            When MODSW is 6, the name of the FACTS device where the
            shunt element’s reactive output is to be controlled. RMIDNT is not used for other
            values of MODSW. RMIDNT is a blank name by default.
            BINIT Initial switched shunt admittance; entered in Mvar at unity voltage. BINIT = 0.0 by
            default.
        Args:
            data:
        """
        self.N1 = ''
        self.N2 = ''
        self.N3 = ''
        self.N4 = ''
        self.N5 = ''
        self.N6 = ''
        self.N7 = ''
        self.N8 = ''
        self.B1 = ''
        self.B2 = ''
        self.B3 = ''
        self.B4 = ''
        self.B5 = ''
        self.B6 = ''
        self.B7 = ''
        self.B8 = ''

        var = [self.N1, self.B1,
               self.N2, self.B2,
               self.N3, self.B3,
               self.N4, self.B4,
               self.N5, self.B5,
               self.N6, self.B6,
               self.N7, self.B7,
               self.N8, self.B8, ]

        if version in [34, 33, 32]:
            self.I, self.MODSW, self.ADJM, self.STAT, self.VSWHI, self.VSWLO, \
             self.SWREM, self.RMPCT, self.RMIDNT, self.BINIT, *var = data[0]
        else:
            logger.append('Shunt not implemented for the version ' + str(version))

    def get_object(self, bus: Bus, logger: list):
        """
        Return GridCal Load object
        Returns:
            Gridcal Load object
        """

        # GL and BL come in MW and MVAr
        # THey must be in siemens
        vv = bus.Vnom**2.0

        if vv == 0:
            logger.append('Voltage equal to zero in shunt conversion!!!')

        g = 0.0
        if self.MODSW in [1, 2]:
            b = self.BINIT * self.RMPCT / 100.0
        else:
            b = self.BINIT

        elm = Shunt(name='Switched shunt ' + str(self.I),
                    G=g, B=b,
                    active=bool(self.STAT))

        return elm


class PSSeShunt:

    def __init__(self, data, version, logger: list):
        """
        I: Bus number, or extended bus name enclosed in single quotes (refer to Extended
            Bus Names). No default allowed.
        ID: One- or two-character uppercase non-blank alphanumeric shunt identifier used to
            distinguish among multiple shunts at bus I. It is recommended that, at buses for
            which a single shunt is present, the shunt be designated as having the shunt identi-
            fier 1. ID = 1 by default.
        STATUS: Shunt status of one for in-service and zero for out-of-service. STATUS = 1 by
            default.
        GL: Active component of shunt admittance to ground; entered in MW at one per unit
            voltage. GL should not include any resistive impedance load, which is entered as
            part of load data. GL = 0.0 by default.
        BL: Reactive component of shunt admittance to ground; entered in Mvar at one per unit
            voltage. BL should not include any reactive impedance load, which is entered as
            part of load data; line charging and line connected shunts, which are entered as part
            of non-transformer branch data; transformer magnetizing admittance, which is
            entered as part of transformer data; or switched shunt admittance, which is entered
            as part of switched shunt data. BL is positive for a capacitor, and negative for a
            reactor or an inductive load. BL = 0.0 by default.
        Args:
            data:
        """
        if version in [33, 32]:
            self.I, self.ID, self.STATUS, self.GL, self.BL = data[0]
        else:
            logger.append('Shunt not implemented for the version ' + str(version))

    def get_object(self, bus: Bus, logger: list):
        """
        Return GridCal Load object
        Returns:
            Gridcal Load object
        """

        # GL and BL come in MW and MVAr
        # They must be in siemens
        vv = bus.Vnom * bus.Vnom

        if vv == 0:
            logger.append('Voltage equal to zero in shunt conversion!!!')

        g = self.GL
        b = self.BL

        elm = Shunt(name=str(self.I) + '_' + str(self.ID),
                    G=g, B=b,
                    active=bool(self.STATUS))

        return elm


class PSSeGenerator:

    def __init__(self, data, version, logger: list):
        """
        I: Bus number, or extended bus name enclosed in single quotes (refer to Extended
            Bus Names). No default allowed.
        ID: One- or two-character uppercase non-blank alphanumeric machine identifier used
            to distinguish among multiple machines at bus I. It is recommended that, at buses
            for which a single machine is present, the machine be designated as having the
            machine identifier 1. ID = 1 by default.
        PG: Generator active power output; entered in MW. PG = 0.0 by default.
        QG: Generator reactive power output; entered in Mvar. QG needs to be entered only if
            the case, as read in, is to be treated as a solved case. QG = 0.0 by default.
        QT: Maximum generator reactive power output; entered in Mvar. For fixed output generators
            (i.e., nonregulating), QT must be equal to the fixed Mvar output. QT = 9999.0
            by default.
        QB: Minimum generator reactive power output; entered in Mvar. For fixed output generators,
            QB must be equal to the fixed Mvar output. QB = -9999.0 by default.
        VS: Regulated voltage setpoint; entered in pu. VS = 1.0 by default.
        IREG: Bus number, or extended bus name enclosed in single quotes, of a remote Type 1
            or 2 bus for which voltage is to be regulated by this plant to the value specified by
            VS. If bus IREG is other than a Type 1 or 2 bus, bus I regulates its own voltage to
            the value specified by VS. IREG is entered as zero if the plant is to regulate its own
            voltage and must be zero for a Type 3 (swing) bus. IREG = 0 by default.
        MBASE: Total MVA base of the units represented by this machine; entered in MVA. This
            quantity is not needed in normal power flow and equivalent construction work, but is
            required for switching studies, fault analysis, and dynamic simulation.
            MBASE = system base MVA by default.
        ZR,ZX: Complex machine impedance, ZSORCE; entered in pu on MBASE base. This data
            is not needed in normal power flow and equivalent construction work, but is required
            for switching studies, fault analysis, and dynamic simulation. For dynamic simula-
            tion, this impedance must be set equal to the unsaturated subtransient impedance
            for those generators to be modeled by subtransient level machine models, and to
            unsaturated transient impedance for those to be modeled by classical or transient
            level models. For short-circuit studies, the saturated subtransient or transient
            impedance should be used. ZR = 0.0 and ZX = 1.0 by default.
        RT,XT: Step-up transformer impedance, XTRAN; entered in pu on MBASE base. XTRAN
            should be entered as zero if the step-up transformer is explicitly modeled as a
            network branch and bus I is the terminal bus. RT+jXT = 0.0 by default.
        GTAP: Step-up transformer off-nominal turns ratio; entered in pu on a system base. GTAP
            is used only if XTRAN is non-zero. GTAP = 1.0 by default.
        STAT: Machine status of one for in-service and zero for out-of-service; STAT = 1 by
            default.
        RMPCT: Percent of the total Mvar required to hold the voltage at the bus controlled by bus I
            that are to be contributed by the generation at bus I; RMPCT must be positive.
        RMPCT: is needed only if IREG specifies a valid remote bus and there is more than
            one local or remote voltage controlling device (plant, switched shunt, FACTS device
            shunt element, or VSC dc line converter) controlling the voltage at bus IREG to a
            setpoint, or IREG is zero but bus I is the controlled bus, local or remote, of one or
            more other setpoint mode voltage controlling devices. RMPCT = 100.0 by default.
        PT: Maximum generator active power output; entered in MW. PT = 9999.0 by default.
        PB: Minimum generator active power output; entered in MW. PB = -9999.0 by default.
        Oi: Owner number (1 through 9999). Each machine may have up to four owners. By
            default, O1 is the owner to which bus I is assigned (refer to Bus Data) and O2, O3,
            and O4 are zero.
        Fi: Fraction of total ownership assigned to owner Oi; each Fi must be positive. The Fi
            values are normalized such that they sum to 1.0 before they are placed in the
            working case. By default, each Fi is 1.0.
        WMOD: Wind machine control mode; WMOD is used to indicate whether a machine is a
            wind machine, and, if it is, the type of reactive power limits to be imposed.
            0 for a machine that is not a wind machine.
            1 for a wind machine for which reactive power limits are specified 
            by QT and QB.
            2 for a wind machine for which reactive power limits are determined from 
            the machine’s active power output and WPF; limits are of equal 
            magnitude and opposite sign
            3 for a wind machine with a fixed reactive power setting determined from 
            the machine’s active power output and WPF; when WPF is positive, 
            the machine’s reactive power has the same sign as its active power; 
            when WPF is negative, the machine’s reactive power has the opposite 
            sign of its active power.
            WMOD = 0 by default.
        WPF: Power factor used in calculating reactive power limits or output when WMOD is 2 or 3.
            WPF = 1.0 by default.
        Args:
            data:
            version:
        """

        self.I = 0
        self.ID = 0
        self.PG = 0
        self.QG = 0
        self.QT = 0
        self.QB = 0
        self.VS = 0
        self.IREG = 0
        self.MBASE = 0
        self.ZR = 0
        self.ZX = 0
        self.RT = 0
        self.XT = 0
        self.GTAP = 0
        self.STAT = 0
        self.RMPCT = 0
        self.PT = 0
        self.PB = 0
        self.O1 = 0
        self.F1 = 0
        self.O2 = 0
        self.F2 = 0
        self.O3 = 0
        self.F3 = 0
        self.O4 = 0
        self.F4 = 0
        self.WMOD = 0
        self.WPF = 0

        var = [self.O1, self.F1,
               self.O2, self.F2,
               self.O3, self.F3,
               self.O4, self.F4]

        length = len(data[0])

        if version in [33, 32, 30]:

            self.I, self.ID, self.PG, self.QG, self.QT, self.QB, self.VS, self.IREG, self.MBASE, \
             self.ZR, self.ZX, self.RT, self.XT, self.GTAP, self.STAT, self.RMPCT, self.PT, self.PB, *var, \
             self.WMOD, self.WPF = data[0]

        elif version in [29]:
            """
            I,ID,PG,QG,QT,QB,VS,IREG,MBASE,
            ZR,ZX,RT,XT,GTAP,STAT,RMPCT,PT,PB,
            O1,F1,...,O4,F4
            """

            self.I, self.ID, self.PG, self.QG, self.QT, self.QB, self.VS, self.IREG, self.MBASE, \
             self.ZR, self.ZX, self.RT, self.XT, self.GTAP, self.STAT, self.RMPCT, self.PT, self.PB, *var = data[0]

        else:
            logger.append('Generator not implemented for version ' + str(version))

    def get_object(self, logger: list):
        """
        Return GridCal Load object
        Returns:
            Gridcal Load object
        """
        name = str(self.I) + '_' + str(self.ID).replace("'", "")
        elm = Generator(name=name,
                        active_power=self.PG,
                        voltage_module=self.VS,
                        Qmin=self.QB,
                        Qmax=self.QT,
                        Snom=self.MBASE,
                        p_max=self.PT,
                        p_min=self.PB,
                        power_prof=None,
                        vset_prof=None,
                        active=bool(self.STAT))

        return elm


class PSSeInductionMachine:

    def __init__(self, data, version, logger: list):
        """

        :param data:
        :param version:
        :param logger:
        """

        if version in [30, 32, 33]:
            '''
            I,ID,STAT,SCODE,DCODE,AREA,ZONE,OWNER,TCODE,BCODE,MBASE,RATEKV,
            PCODE,PSET,H,A,B,D,E,RA,XA,XM,R1,X1,R2,X2,X3,E1,SE1,E2,SE2,IA1,IA2,
            XAMULT
            '''
            self.I, self.ID, self.STAT, self.SCODE, self.DCODE, self.AREA, self.ZONE, self.OWNER, \
            self.TCODE, self.BCODE, self.MBASE, self.RATEKV = data[0]

            self.PCODE, self.PSET, self.H, self.A, self.B, self.D, self.E, self.RA, self.XA, self.XM, self.R1, \
            self.X1, self.R2, self.X2, self.X3, self.E1, self.SE1, self.E2, self.SE2, self.IA1, self.IA2 = data[1]

            self.XAMULT = data[2]
        else:
            logger.append('Induction machine not implemented for version ' + str(version))

    def get_object(self, logger: list):
        """
        Return GridCal Load object
        Returns:
            Gridcal Load object
        """

        elm = Generator(name=str(self.I) + '_' + str(self.ID),
                        active_power=self.PSET,
                        voltage_module=self.RATEKV,
                        Snom=self.MBASE,
                        active=bool(self.STAT))

        return elm


class PSSeBranch:

    def __init__(self, data, version, logger: list):
        """
        I: Branch from bus number, or extended bus name enclosed in single quotes (refer to
            Extended Bus Names). No default allowed.
        J: Branch to bus number, or extended bus name enclosed in single quotes.
        CKT: One- or two-character uppercase non-blank alphanumeric branch circuit identifier;
            the first character of CKT must not be an ampersand ( & ); refer to Multi-Section
            Line Grouping Data. If the first character of CKT is an at sign ( @ ), the branch is
            treated as a breaker; if it is an asterisk ( * ), it is treated as a switch (see Section
            6.17.2, Outage Statistics Data File Contents). Unless it is a breaker or switch, it is
            recommended that single circuit branches be designated as having the circuit identifier 1.
            CKT = 1 by default.
        R: Branch resistance; entered in pu. A value of R must be entered for each branch.
        X: Branch reactance; entered in pu. A non-zero value of X must be entered for each
            branch. Refer to Zero Impedance Lines for details on the treatment of branches as
            zero impedance lines.
        B: Total branch charging susceptance; entered in pu. B = 0.0 by default.
        RATEA: First rating; entered in either MVA or current expressed as MVA, according to the
            value specified for NXFRAT specified on the first data record (refer to Case Identification Data).
            RATEA = 0.0 (bypass check for this branch; this branch will not be included in any
            examination of circuit loading) by default. Refer to activity RATE.
        RATEB: Second rating; entered in either MVA or current expressed as MVA, according to
            the value specified for NXFRAT specified on the first data record (refer to Case
            Identification Data). RATEB = 0.0 by default.
        RATEC: Third rating; entered in either MVA or current expressed as MVA, according to the
            value specified for NXFRAT specified on the first data record (refer to Case Identification Data).
            RATEC = 0.0 by default.
            When specified in units of current expressed as MVA, ratings are entered as:
            MVArated = sqrt(3) x Ebase x Irated x 10-6
            where:
                Ebase is the base line-to-line voltage in volts of the buses to which the terminal of the branch
                    is connected
                Irated is the branch rated phase current in amperes.
        GI,BI: Complex admittance of the line shunt at the bus I end of the branch; entered in pu.
            BI is negative for a line connected reactor and positive for line connected capacitor.
            GI + jBI = 0.0 by default.
        GJ,BJ: Complex admittance of the line shunt at the bus J end of the branch; entered in pu.
            BJ is negative for a line connected reactor nd positive for line connected capacitor.
            GJ + jBJ = 0.0 by default.
        ST: Branch status of one for in-service and zero for out-of-service; ST = 1 by default.
        MET: Metered end flag;
            <1 to designate bus I as the metered end
            >2 to designate bus J as the metered end.
            MET = 1 by default.
        LEN: Line length; entered in user-selected units. LEN = 0.0 by default.
        Oi: Owner number (1 through 9999). Each branch may have up to four owners. By
            default, O1 is the owner to which bus I is assigned (refer to Bus Data) and O2, O3,
            and O4 are zero.
        Fi: Fraction of total ownership assigned to owner Oi; each Fi must be positive. The Fi
            values are normalized such that they sum to 1.0 before they are placed in the
            working case. By default, each Fi is 1.0.
        Args:
            data:
            version:
        """

        self.O1 = ''
        self.F1 = ''
        self.O2 = ''
        self.F2 = ''
        self.O3 = ''
        self.F3 = ''
        self.O4 = ''
        self.F4 = ''
        var = [self.O1, self.F1, self.O2, self.F2, self.O3, self.F3, self.O4, self.F4]

        if version in [33, 32]:

            '''
            I,J,CKT,R,X,B,RATEA,RATEB,RATEC,GI,BI,GJ,BJ,ST,MET,LEN,O1,F1,...,O4,F4
            '''

            self.I, self.J, self.CKT, self.R, self.X, self.B, self.RATEA, self.RATEB, self.RATEC, \
             self.GI, self.BI, self.GJ, self.BJ, self.ST, self.MET, self.LEN, *var = data[0]

        elif version in [29, 30]:
            """
            v29, v30
            I,J,CKT,R,X,B,RATEA,RATEB,RATEC,GI,BI,GJ,BJ,ST,LEN,01,F1,...,04,F4
            """

            self.I, self.J, self.CKT, self.R, self.X, self.B, self.RATEA, self.RATEB, self.RATEC, \
             self.GI, self.BI, self.GJ, self.BJ, self.ST, self.LEN, *var = data[0]

        else:

            logger.append('Branch not implemented for version ' + str(version))

    def get_object(self, psse_bus_dict, Sbase, logger: list):
        """
        Return GridCal branch object
        Args:
            psse_bus_dict: Dictionary that relates PSSe bus indices with GridCal Bus objects

        Returns:
            Gridcal Branch object
        """
        i = abs(self.I)
        j = abs(self.J)
        bus_from = psse_bus_dict[i]
        bus_to = psse_bus_dict[j]
        name = str(i) + '_' + str(j) + '_' + str(self.CKT).replace("'", "")

        branch = Branch(bus_from=bus_from, bus_to=bus_to,
                        name=name,
                        r=self.R,
                        x=self.X,
                        g=1e-20,
                        b=self.B,
                        rate=max(self.RATEA, self.RATEB, self.RATEC),
                        tap=1,
                        shift_angle=0,
                        active=bool(self.ST),
                        mttf=0,
                        mttr=0,
                        length=self.LEN,
                        branch_type=BranchType.Line)
        return branch


class PSSeTwoTerminalDCLine:

    def __init__(self, data, version, logger: list):
        """

        :param data:
        :param version:
        :param logger:



        NAME	The non-blank alphanumeric identifier assigned to this dc line. Each two-terminal dc line must have a
        unique NAME. NAME may be up to twelve characters and may contain any combination of blanks, uppercase letters,
        numbers and special characters. NAME must be enclosed in single or double quotes if it contains any blanks or
        special characters. No default allowed.

        MDC	Control mode: 0 for blocked, 1 for power, 2 for current. MDC = 0 by default.

        RDC	The dc line resistance; entered in ohms. No default allowed.

        SETVL	Current (amps) or power (MW) demand. When MDC is one, a positive value of SETVL specifies desired power
        at the rectifier and a negative value specifies desired inverter power. No default allowed.

        VSCHD	Scheduled compounded dc voltage; entered in kV. No default allowed.

        VCMOD	Mode switch dc voltage; entered in kV. When the inverter dc voltage falls below this value and the
        line is in power control mode (i.e., MDC = 1), the line switches to current control mode with a desired
        current corresponding to the desired power at scheduled dc voltage. VCMOD = 0.0 by default.

        RCOMP	Compounding resistance; entered in ohms. Gamma and/or TAPI is used to attempt to hold the compounded
        voltage (VDCI + DCCURRCOMP) at VSCHD. To control the inverter end dc voltage VDCI, set RCOMP to zero;
        to control the rectifier end dc voltage VDCR, set RCOMP to the dc line resistance, RDC; otherwise,
        set RCOMP to the appropriate fraction of RDC. RCOMP = 0.0 by default.

        DELTI	Margin entered in per unit of desired dc power or current. This is the fraction by which the order is
        reduced when ALPHA is at its minimum and the inverter is controlling the line current. DELTI = 0.0 by default.

        METER	Metered end code of either R (for rectifier) or I (for inverter). METER = I by default.

        DCVMIN	Minimum compounded dc voltage; entered in kV. Only used in constant gamma operation
        (i.e., when ANMXI = ANMNI) when TAPI is held constant and an ac transformer tap is adjusted to control
        dc voltage (i.e., when IFI, ITI, and IDI specify a twowinding transformer). DCVMIN = 0.0 by default.

        CCCITMX	Iteration limit for capacitor commutated two-terminal dc line Newton solution procedure.
        CCCITMX = 20 by default.

        CCCACC	Acceleration factor for capacitor commutated two-terminal dc line Newton solution procedure.
        CCCACC = 1.0 by default.

        IPR	Rectifier converter bus number, or extended bus name enclosed in single quotes (refer to Extended Bus
        Names). No default allowed.

        NBR	Number of bridges in series (rectifier). No default allowed.

        ANMXR	Nominal maximum rectifier firing angle; entered in degrees. No default allowed.

        ANMNR	Minimum steady-state rectifier firing angle; entered in degrees. No default allowed.

        RCR	Rectifier commutating transformer resistance per bridge; entered in ohms. No default allowed.

        XCR	Rectifier commutating transformer reactance per bridge; entered in ohms. No default allowed.

        EBASR	Rectifier primary base ac voltage; entered in kV. No default allowed.

        TRR	Rectifier transformer ratio. TRR = 1.0 by default.

        TAPR	Rectifier tap setting. TAPR = 1.0 by default.

        If no two-winding transformer is specified by IFR, ITR, and IDR, TAPR is adjusted to keep alpha within limits;
        otherwise, TAPR is held fixed and this transformer’s tap ratio is adjusted. The adjustment logic assumes that
        the rectifier converter bus is on the Winding 2 side of the transformer. The limits TMXR and TMNR specified
        here are used; except for the transformer control mode flag (COD1 of Transformer Data), the ac tap adjustment
        data is ignored.

        TMXR	Maximum rectifier tap setting. TMXR = 1.5 by default.

        TMNR	Minimum rectifier tap setting. TMNR = 0.51 by default.

        STPR	Rectifier tap step; must be positive. STPR = 0.00625 by default.

        ICR	Rectifier firing angle measuring bus number, or extended bus name enclosed in single quotes
        (refer to Extended Bus Names). The firing angle and angle limits used inside the dc model are adjusted by
        the difference between the phase angles at this bus and the ac/dc interface (i.e., the converter bus, IPR).
        ICR = 0 by default.

        IFR	Winding 1 side from bus number, or extended bus name enclosed in single quotes, of a two-winding
        transformer. IFR = 0 by default.

        ITR	Winding 2 side to bus number, or extended bus name enclosed in single quotes, of a two-winding
        transformer. ITR = 0 by default.

        IDR	Circuit identifier; the branch described by IFR, ITR, and IDR must have been entered as a two-winding
        transformer; an ac transformer may control at most only one dc converter. IDR = '1' by default.

        XCAPR	Commutating capacitor reactance magnitude per bridge; entered in ohms. XCAPR = 0.0 by default.


        """

        if version in [33, 34]:
            '''
            'NAME',MDC,RDC,SETVL,VSCHD,VCMOD,RCOMP,DELTI,METER,DCVMIN,CCCITMX,CCCACC
            IPR,NBR,ANMXR,ANMNR,RCR,XCR,EBASR,TRR,TAPR,TMXR,TMNR,STPR,ICR,IFR,ITR,IDR,XCAPR
            IPI,NBI,ANMXI,ANMNI,RCI,XCI,EBASI,TRI,TAPI,TMXI,TMNI,STPI,ICI,IFI,ITI,IDI,XCAPI 
            '''

            self.NAME, self.MDC, self.RDC, self.SETVL, self.VSCHD, self.VCMOD, self.RCOMP, self.DELTI, self.METER, \
             self.DCVMIN, self.CCCITMX, self.CCCACC = data[0]

            self.IPR, self.NBR, self.ANMXR, self.ANMNR, self.RCR, self.XCR, self.EBASR, self.TRR, self.TAPR, \
             self.TMXR, self.TMNR, self.STPR, self.ICR, self.IFR, self.ITR, self.IDR, self.XCAPR = data[1]

            self.IPI, self.NBI, self.ANMXI, self.ANMNI, self.RCI, self.XCI, self.EBASI, self.TRI, self.TAPI, \
             self.TMXI, self.TMNI, self.STPI, self.ICI, self.IFI, self.ITI, self.IDI, self.XCAPI = data[2]

        elif version == 29:
            '''
            I,MDC,RDC,SETVL,VSCHD,VCMOD,RCOMP,DELTI,METER,DCVMIN,CCCITMX,CCCACC
            IPR,NBR,ALFMX,ALFMN,RCR,XCR,EBASR,TRR,TAPR,TMXR,TMNR,STPR,ICR,IFR,ITR,IDR,XCAPR
            IPI,NBI,GAMMX,GAMMN,RCI,XCI,EBASI,TRI,TAPI,TMXI,TMNI,STPI,ICI,IFI,ITI,IDI,XCAPI
            '''

            self.I, self.MDC, self.RDC, self.SETVL, self.VSCHD, self.VCMOD, self.RCOMP, self.DELTI, self.METER, \
             self.DCVMIN, self.CCCITMX, self.CCCACC = data[0]

            self.IPR, self.NBR, self.ANMXR, self.ANMNR, self.RCR, self.XCR, self.EBASR, self.TRR, self.TAPR, \
             self.TMXR, self.TMNR, self.STPR, self.ICR, self.IFR, self.ITR, self.IDR, self.XCAPR = data[1]

            self.IPI, self.NBI, self.ANMXI, self.ANMNI, self.RCI, self.XCI, self.EBASI, self.TRI, self.TAPI, \
             self.TMXI, self.TMNI, self.STPI, self.ICI, self.IFI, self.ITI, self.IDI, self.XCAPI = data[2]

            self.NAME = str(self.I)
        else:
            logger.append('Version ' + str(version) + ' not implemented for DC Lines')

    def get_object(self, psse_bus_dict, Sbase, logger: list):
        """
        GEt equivalent object
        :param psse_bus_dict:
        :param logger:
        :return:
        """
        bus1 = psse_bus_dict[abs(self.IPR)]
        bus2 = psse_bus_dict[abs(self.IPI)]

        if self.MDC == 1:
            # SETVL is in MW
            specified_power = self.SETVL
        elif self.MDC == 2:
            # SETVL is in A, specified_power in MW
            specified_power = self.SETVL * self.VSCHD / 1000.0
        else:
            # doesn't say, so I expect it to be MW
            specified_power = self.SETVL

        z_base = self.VSCHD * self.VSCHD / Sbase
        r_pu = self.RDC / z_base

        name1 = self.NAME.replace("'", "").replace('/', '').strip()
        name = str(self.IPR) + '_' + str(self.IPI) + '_' + name1 + '_DC_2_terminals'

        obj = Branch(bus_from=bus1,
                     bus_to=bus2,
                     name=name,
                     r=r_pu,
                     rate=specified_power,
                     branch_type=BranchType.DCLine)
        return obj


class PSSeVscDCLine:

    def __init__(self, data, version, logger: list):
        """

        :param data:
        :param version:
        :param logger:

        NAME	The non-blank alphanumeric identifier assigned to this dc line. Each VSC dc line must have a unique NAME. NAME may be up to twelve characters and may contain any combination of blanks, uppercase letters, numbers and special characters. NAME must be enclosed in single or double quotes if it contains any blanks or special characters. No default allowed.
        MDC	Control mode: 0 for out-of-service, 1 for in-service. MDC = 1 by default.
        RDC	The dc line resistance; entered in ohms. RDC must be positive. No default allowed.
        Oi An owner number (1 through 9999). Each VSC dc line may have up to four owners. By default, O1 is 1, and O2, O3 and O4 are zero.
        Fi	The fraction of total ownership assigned to owner Oi; each Fi must be positive. The Fi values are normalized such that they sum to 1.0 before they are placed in the working case. By default, each Fi is 1.0.

        IBUS	Converter bus number, or extended bus name enclosed in single quotes (refer to Extended Bus Names). No default allowed.

        TYPE	Code for the type of converter dc control:
        0	 for converter out-of-service 1	 for dc voltage control 2	 for MW control.
        When both converters are in-service, exactly one converter of each VSC dc line must be TYPE 1. No default allowed.
        MODE	Converter ac control mode:
        1	for ac voltage control
        2	for fixed ac power factor.
        MODE = 1 by default.
        DCSET	Converter dc setpoint. For TYPE = 1, DCSET is the scheduled dc voltage on the dc side of the converter bus; entered in kV. For TYPE = 2, DCSET is the power demand, where a positive value specifies that the converter is feeding active power into the ac network at bus IBUS, and a negative value specifies that the converter is withdrawing active power from the ac network at bus IBUS; entered in MW. No default allowed.
        ACSET	Converter ac setpoint. For MODE = 1, ACSET is the regulated ac voltage setpoint; entered in pu. For MODE = 2, ACSET is the power factor setpoint. ACSET = 1.0 by default.
        Aloss,
        Bloss	Coefficients of the linear equation used to calculate converter losses:
        KWconv loss = Aloss + (Idc * Bloss)
        Aloss is entered in kW. Bloss is entered in kW/amp. Aloss = Bloss = 0.0 by default.
        MINloss	Minimum converter losses; entered in kW. MINloss = 0.0 by default.
        SMAX	Converter MVA rating; entered in MVA. SMAX = 0.0 to allow unlimited converter MVA loading. SMAX = 0.0 by default.
        IMAX	Converter ac current rating; entered in amps. IMAX = 0.0 to allow unlimited converter current loading. If a positive IMAX is specified, the base voltage assigned to bus IBUS must be positive. IMAX = 0.0 by default.
        PWF	Power weighting factor fraction (0.0 < PWF < 1.0) used in reducing the active power order and either the reactive power order (when MODE is 2) or the reactive power limits (when MODE is 1) when the converter MVA or current rating is violated. When PWF is 0.0, only the active power is reduced; when PWF is 1.0, only the reactive power is reduced; otherwise, a weighted reduction of both active and reactive power is applied. PWF = 1.0 by default.
        MAXQ	Reactive power upper limit; entered in Mvar. A positive value of reactive power indicates reactive power
                flowing into the ac network from the converter; a negative value of reactive power indicates reactive
                power withdrawn from the ac network. Not used if MODE = 2. MAXQ = 9999.0 by default.
        MINQ	Reactive power lower limit; entered in Mvar. A positive value of reactive power indicates reactive power flowing into the ac network from the converter; a negative value of reactive power indicates reactive power withdrawn from the ac network.
                Not used if MODE = 2. MINQ = -9999.0 by default.
        REMOT	Bus number, or extended bus name enclosed in single quotes (refer to Extended Bus Names), of a remote
                Type 1 or 2 bus for which voltage is to be regulated by this converter to the value specified by ACSET.
                If bus REMOT is other than a Type 1 or 2 bus, bus IBUS regulates its own voltage to the value specified
                by ACSET.
        REMOT   is entered as zero if the converter is to regulate its own voltage. Not used if MODE = 2. REMOT = 0 by
                default.
        RMPCT	Percent of the total Mvar required to hold the voltage at the bus controlled by bus IBUS that is to be
                contributed by this VSC; RMPCT must be positive. RMPCT is needed only if REMOT specifies a valid remote
                bus and there is more than one local or remote voltage controlling device (plant, switched shunt, FACTS
                device shunt element, or VSC dc line converter) controlling the voltage at bus REMOT to a setpoint, or
                REMOT is zero but bus IBUS is the controlled bus, local or remote, of one or more other setpoint mode
                voltage controlling devices. Not used if MODE = 2. RMPCT = 100.0 by default.
        """
        self.O1 = ''
        self.F1 = ''
        self.O2 = ''
        self.F2 = ''
        self.O3 = ''
        self.F3 = ''
        self.O4 = ''
        self.F4 = ''
        var = [self.O1, self.F1, self.O2, self.F2, self.O3, self.F3, self.O4, self.F4]

        if version in [33, 34]:

            '''
            NAME, MDC, RDC, O1, F1, ... O4, F4
            IBUS,TYPE,MODE,DCSET,ACSET,ALOSS,BLOSS,MINLOSS,SMAX,IMAX,PWF,MAXQ,MINQ,REMOT,RMPCT
            IBUS,TYPE,MODE,DCSET,ACSET,ALOSS,BLOSS,MINLOSS,SMAX,IMAX,PWF,MAXQ,MINQ,REMOT,RMPCT
            '''

            self.NAME, self.MDC, self.RDC, *var = data[0]

            self.IBUS1, self.TYPE1, self.MODE1, self.DCSET1, self.ACSET1, self.ALOSS1, self.BLOSS1, self.MINLOSS1, \
             self.SMAX1, self.IMAX1, self.PWF1, self.MAXQ1, self.MINQ1, self.REMOT1, self.RMPCT1 = data[1]

            self.IBUS2, self.TYPE2, self.MODE2, self.DCSET2, self.ACSET2, self.ALOSS2, self.BLOSS2, self.MINLOSS2, \
             self.SMAX2, self.IMAX2, self.PWF2, self.MAXQ2, self.MINQ2, self.REMOT2, self.RMPCT2 = data[2]

        elif version == 29:

            '''
            ’NAME’, MDC, RDC, O1, F1, ... O4, F4
            IBUS,TYPE,MODE,DCSET,ACSET,ALOSS,BLOSS,MINLOSS,SMAX,IMAX,PWF,MAXQ,MINQ,REMOT,RMPCT
            IBUS,TYPE,MODE,DCSET,ACSET,ALOSS,BLOSS,MINLOSS,SMAX,IMAX,PWF,MAXQ,MINQ,REMOT,RMPCT
            '''

            self.NAME, self.MDC, self.RDC, *var = data[0]

            self.IBUS1, self.TYPE1, self.MODE1, self.DCSET1, self.ACSET1, self.ALOSS1, self.BLOSS1, self.MINLOSS1, \
             self.SMAX1, self.IMAX1, self.PWF1, self.MAXQ1, self.MINQ1, self.REMOT1, self.RMPCT1 = data[1]

            self.IBUS2, self.TYPE2, self.MODE2, self.DCSET2, self.ACSET2, self.ALOSS2, self.BLOSS2, self.MINLOSS2, \
             self.SMAX2, self.IMAX2, self.PWF2, self.MAXQ2, self.MINQ2, self.REMOT2, self.RMPCT2 = data[2]

        else:
            logger.append('Version ' + str(version) + ' not implemented for DC Lines')

    def get_object(self, psse_bus_dict, Sbase, logger: list):
        """
        GEt equivalent object
        :param psse_bus_dict:
        :param logger:
        :return:
        """
        bus1 = psse_bus_dict[abs(self.IBUS1)]
        bus2 = psse_bus_dict[abs(self.IBUS2)]

        obj = Branch(bus_from=bus1,
                     bus_to=bus2,
                     name=self.NAME + '_DC_2_terminals',
                     r=self.RDC,
                     rate=max(self.SMAX1, self.SMAX2))
        return obj


class PSSeTransformer:

    def __init__(self, data, version, logger: list):
        """
        I The bus number, or extended bus name enclosed in single quotes (refer to
            Extended Bus Names), of the bus to which Winding 1 is connected. The trans-
            former’s magnetizing admittance is modeled on Winding 1. Winding 1 is the only
            winding of a two-winding transformer for which tap ratio or phase shift angle may be
            adjusted by the power flow solution activities; any winding(s) of a three-winding
            transformer may be adjusted. No default is allowed.
        J The bus number, or extended bus name enclosed in single quotes, of the bus to
            which Winding 2 is connected. No default is allowed.
        K The bus number, or extended bus name enclosed in single quotes, of the bus to
            which Winding 3 is connected. Zero is used to indicate that no third winding is
            present (i.e., that a two-winding rather than a three-winding transformer is being
            specified). K = 0 by default.
        CKT One- or two-character uppercase non-blank alphanumeric transformer circuit identi-
            fier; the first character of CKT must not be an ampersand ( & ), at sign ( @ ), or
            asterisk ( * ); refer to Multi-Section Line Grouping Data and Section 6.17.2, Outage
            Statistics Data File Contents. CKT = 1 by default.
        CW The winding data I/O code defines the units in which the turns ratios WINDV1,
            WINDV2 and WINDV3 are specified (the units of RMAn and RMIn are also
            governed by CW when |CODn| is 1 or 2):
            1 for off-nominal turns ratio in pu of winding bus base voltage
            2 for winding voltage in kV
            3 for off-nominal turns ratio in pu of nominal winding voltage, 
            NOMV1, NOMV2 and NOMV3.
            CW = 1 by default.
        CZ  The impedance data I/O code defines the units in which the winding impedances
            R1-2, X1-2, R2-3, X2-3, R3-1 and X3-1 are specified:

            1 for resistance and reactance in pu on system MVA base and  winding voltage base

            2 for resistance and reactance in pu on a specified MVA base and winding voltage base

            3 for transformer load loss in watts and impedance magnitude in pu on a specified
              MVA base and winding voltage base.

            In specifying transformer leakage impedances, the base voltage values are always
            the nominal winding voltages that are specified on the third, fourth and fifth records
            of the transformer data block (NOMV1, NOMV2 and NOMV3). If the default NOMVn
            is not specified, it is assumed to be identical to the winding n bus base voltage.
            CZ = 1 by default.
        CM The magnetizing admittance I/O code defines the units in which MAG1 and MAG2 are specified:
            1 for complex admittance in pu on system MVA base and Winding 1 
            bus voltage base
            2 for no load loss in watts and exciting current in pu on Winding 1 to 
            two MVA base (SBASE1-2) and nominal Winding 1 voltage, NOMV1.
            CM = 1 by default.
        MAG1, MAG2: The transformer magnetizing admittance connected to ground at bus I.
            When CM is 1, MAG1 and MAG2 are the magnetizing conductance and suscep-
            tance, respectively, in pu on system MVA base and Winding 1 bus voltage base.
            When a non-zero MAG2 is specified, it should be entered as a negative quantity.
            When CM is 2, MAG1 is the no load loss in watts and MAG2 is the exciting current
            in pu on Winding 1 to two MVA base (SBASE1-2) and nominal Winding 1 voltage
            (NOMV1). For three-phase transformers or three-phase banks of single phase
            transformers, MAG1 should specify the three-phase no-load loss. When a non-zero
            MAG2 is specified, it should be entered as a positive quantity.
            MAG1 = 0.0 and MAG2 = 0.0 by default.
        NMETR The non-metered end code of either 1 (for the Winding 1 bus) or 2 (for the Winding 2 bus).
            In addition, for a three-winding transformer, 3 (for the Winding 3 bus) is a valid
            specification of NMETR. NMETR = 2 by default.
        NAME Alphanumeric identifier assigned to the transformer. NAME may be up to twelve
            characters and may contain any combination of blanks, uppercase letters, numbers
            and special characters. NAME must be enclosed in single or double quotes if it
            contains any blanks or special characters. NAME is twelve blanks by default.
        STAT Transformer status of one for in-service and zero for out-of-service.
            In addition, for a three-winding transformer, the following values of STAT provide for
            one winding out-of-service with the remaining windings in-service:
            2 -> for only Winding 2 out-of-service
            3 -> for only Winding 3 out-of-service
            4 -> for only Winding 1 out-of-service
            STAT = 1 by default.
        Oi: An owner number (1 through 9999). Each transformer may have up to four owners.
            By default, O1 is the owner to which bus I is assigned and O2, O3, and O4 are zero.
        Fi: The fraction of total ownership assigned to owner Oi; each Fi must be positive. The
            Fi values are normalized such that they sum to 1.0 before they are placed in the
            working case. By default, each Fi is 1.0.
        VECGRP: Alphanumeric identifier specifying vector group based on transformer winding
            connections and phase angles. VECGRP value is used for information purpose
            only. VECGRP is 12 blanks by default

        ----------------------------------------------------------------------------------------------
        The first three data items on the second record are read for both two- and three-winding trans-
        formers; the remaining data items are used only for three-winding transformers:

        R1-2, X1-2 The measured impedance of the transformer between the buses to which its first
            and second windings are connected.
            When CZ is 1, they are the resistance and reactance, respectively, in pu on system
            MVA base and winding voltage base.
            When CZ is 2, they are the resistance and reactance, respectively, in pu on Winding
            1 to 2 MVA base (SBASE1-2) and winding voltage base.
            When CZ is 3, R1-2 is the load loss in watts, and X1-2 is the impedance magnitude
            in pu on Winding 1 to 2 MVA base (SBASE1-2) and winding voltage base. For
            three-phase transformers or three-phase banks of single phase transformers, R1-2
            should specify the three-phase load loss.
            R1-2 = 0.0 by default, but no default is allowed for X1-2.
        SBASE1-2 The Winding 1 to 2 three-phase base MVA of the transformer. SBASE1-2 = SBASE
            (the system base MVA) by default.
        R2-3, X2-3 The measured impedance of a three-winding transformer between the buses to
            which its second and third windings are connected; ignored for a two-winding
            transformer.
            When CZ is 1, they are the resistance and reactance, respectively, in pu on system
            MVA base and winding voltage base.
            When CZ is 2, they are the resistance and reactance, respectively, in pu on Winding
            2 to 3 MVA base (SBASE2-3) and winding voltage base.
            When CZ is 3, R2-3 is the load loss in watts, and X2-3 is the impedance magnitude
            in pu on Winding 2 to 3 MVA base (SBASE2-3) and winding voltage base. For
            three-phase transformers or three-phase banks of single phase transformers, R2-3
            should specify the three-phase load loss.
            R2-3 = 0.0 by default, but no default is allowed for X2-3.
        SBASE2-3 The Winding 2 to 3 three-phase base MVA of a three-winding transformer; ignored
            for a two-winding transformer. SBASE2-3 = SBASE (the system base MVA) by
            default.
        R3-1, X3-1 The measured impedance of a three-winding transformer between the buses to
            which its third and first windings are connected; ignored for a two-winding
            transformer.
            When CZ is 1, they are the resistance and reactance, respectively, in pu on system
            MVA base and winding voltage base.
            When CZ is 2, they are the resistance and reactance, respectively, in pu on Winding
            3 to 1 MVA base (SBASE3-1) and winding voltage base.
            When CZ is 3, R3-1 is the load loss in watts, and X3-1 is the impedance magnitude
            in pu on Winding 3 to 1 MVA base (SBASE3-1) and winding voltage base. For
            three-phase transformers or three-phase banks of single phase transformers, R3-1
            should specify the three-phase load loss.
            R3-1 = 0.0 by default, but no default is allowed for X3-1.
        SBASE3-1 The Winding 3 to 1 three-phase base MVA of a three-winding transformer; ignored
            for a two-winding transformer. SBASE3-1 = SBASE (the system base MVA) by

        VMSTAR The voltage magnitude at the hidden star point bus; entered in pu. VMSTAR = 1.0
            by default.
        ANSTAR The bus voltage phase angle at the hidden star point bus; entered in degrees.
            ANSTAR = 0.0 by default.

        ----------------------------------------------------------------------------------------------
        All data items on the third record are read for both two- and three-winding transformers:

        WINDV1: When CW is 1, WINDV1 is the Winding 1 off-nominal turns ratio in pu of Winding 1
            bus base voltage; WINDV1 = 1.0 by default.
            When CW is 2, WINDV1 is the actual Winding 1 voltage in kV; WINDV1 is equal to
            the base voltage of bus I by default.
            When CW is 3, WINDV1 is the Winding 1 off-nominal turns ratio in pu of nominal
            Winding 1 voltage, NOMV1; WINDV1 = 1.0 by default.
        NOMV1 The nominal (rated) Winding 1 voltage base in kV, or zero to indicate that nominal
            Winding 1 voltage is assumed to be identical to the base voltage of bus I. NOMV1 is
            used in converting magnetizing data between physical units and per unit admittance
            values when CM is 2. NOMV1 is used in converting tap ratio data between values in
            per unit of nominal Winding 1 voltage and values in per unit of Winding 1 bus base
            voltage when CW is 3. NOMV1 = 0.0 by default.
        ANG1 The winding one phase shift angle in degrees. For a two-winding transformer,
            ANG1 is positive when the winding one bus voltage leads the winding two bus
            voltage; for a three-winding transformer, ANG1 is positive when the winding one
            bus voltage leads the T (or star) point bus voltage. ANG1 must be greater than -
            180.0o and less than or equal to +180.0o. ANG1 = 0.0 by default.
        RATA1, RATB1, RATC1: Winding 1’s three three-phase ratings, entered in either MVA or current expressed
            as MVA, according to the value specified for XFRRAT specified on the first data
            record (refer to Case Identification Data). RATA1 = 0.0, RATB1 = 0.0 and
            RATC1 = 0.0 (bypass loading limit check for this transformer winding) by default.
        COD1 The transformer control mode for automatic adjustments of the Winding 1 tap or
            phase shift angle during power flow solutions:
                0 for no control (fixed tap and fixed phase shift)
                ±1  for voltage control
                ±2  for reactive power flow control
                ±3  for active power flow control
                ±4  for control of a dc line quantity (valid only for two-winding  transformers)
                ±5  for asymmetric active power flow control.
            If the control mode is entered as a positive number, automatic adjustment of this
            transformer winding is enabled when the corresponding adjustment is activated
            during power flow solutions; a negative control mode suppresses the automatic
            adjustment of this transformer winding. COD1 = 0 by default.

        CONT1: The bus number, or extended bus name enclosed in single quotes (refer to
            Extended Bus Names), of the bus for which voltage is to be controlled by the trans-
            former turns ratio adjustment option of the power flow solution activities when
            COD1 is 1. CONT1 should be non-zero only for voltage controlling transformer
            windings.
            CONT1 may specify a bus other than I, J, or K; in this case, the sign of CONT1
            defines the location of the controlled bus relative to the transformer winding. If
            CONT1 is entered as a positive number, or a quoted extended bus name, the ratio
            is adjusted as if bus CONT1 is on the Winding 2 or Winding 3 side of the trans-
            former; if CONT1 is entered as a negative number, or a quoted extended bus name
            with a minus sign preceding the first character, the ratio is adjusted as if bus
            |CONT1| is on the Winding 1 side of the transformer. CONT1 = 0 by default.
        RMA1, RMI1:  When |COD1| is 1, 2 or 3, the upper and lower limits, respectively, of one of the
            following:
            • Off-nominal turns ratio in pu of Winding 1 bus base voltage when |COD1| is
            1 or 2 and CW is 1; RMA1 = 1.1 and RMI1 = 0.9 by default.
            • Actual Winding 1 vo ltage in kV when |COD1| is 1 o r 2 and CW is 2 . No
            default is allowed.
            • Off-nominal turns ratio in pu of nominal Winding 1 voltage (NOMV1) when
            |COD1| is 1 or 2 and CW is 3; RMA1 = 1.1 and RMI1 = 0.9 by default.
            • Phase shift angle in degrees when |COD1| is 3. No default is allowed.
            Not used when |COD1| is 0 or 4; RMA1 = 1.1 and RMI1 = 0.9 by default.
        VMA1, VMI1:  When |COD1| is 1, 2 or 3, the upper and lower limits, respectively, of one of the
            following:
            • Voltage at the controlled bus (bus |CONT1|) in pu when |COD1| is 1. 
            VMA1 = 1.1 and VMI1 = 0.9 by default.
            • Reactive power flow into the transformer at the Winding 1 bus end in Mvar
            when |COD1| is 2. No default is allowed.
            • Active power flow into the transformer at the Winding 1 bus end in MW when
            |COD1| is 3. No default is allowed.
            Not used when |COD1| is 0 or 4; VMA1 = 1.1 and VMI1 = 0.9 by default.
        NTP1: The number of tap positions available; used when COD1 is 1 or 2. NTP1 must be
            between 2 and 9999. NTP1 = 33 by default.
        TAB1: The number of a transformer impedance correction table if this transformer
            winding’s impedance is to be a function of either off-nominal turns ratio or phase
            shift angle (refer to Transformer Impedance Correction Tables), or 0 if no trans-
            former impedance correction is to be applied to this transformer winding. TAB1 = 0
            by default.
        CR1, CX1: The load drop compensation impedance for voltage controlling transformers
            entered in pu on system base quantities; used when COD1 is 1. CR1 + j CX1 = 0.0
            by default.
        CNXA1: Winding connection angle in degrees; used when COD1 is 5. There are no restrictions
            on the value specified for CNXA1; if it is outside of the range from -90.0 to
            +90.0, CNXA1 is normalized to within this range. CNXA1 = 0.0 by default.

        ----------------------------------------------------------------------------------------------
        The first two data items on the fourth record are read for both two- and three-winding transformers;
        the remaining data items are used only for three-winding transformers:

        WINDV2:  When CW is 1, WINDV2 is the Winding 2 off-nominal turns ratio in pu of Winding 2
            bus base voltage; WINDV2 = 1.0 by default.
            When CW is 2, WINDV2 is the actual Winding 2 voltage in kV; WINDV2 is equal to
            the base voltage of bus J by default.
            When CW is 3, WINDV2 is the Winding 2 off-nominal turns ratio in pu of nominal
            Winding 2 voltage, NOMV2; WINDV2 = 1.0 by default.
        NOMV2 The nominal (rated) Winding 2 voltage base in kV, or zero to indicate that nominal
            Winding 2 voltage is assumed to be identical to the base voltage of bus J. NOMV2
            is used in converting tap ratio data between values in per unit of nominal Winding 2
            voltage and values in per unit of Winding 2 bus base voltage when CW is 3.
            NOMV2 = 0.0 by default.
        ANG2 The winding two phase shift angle in degrees. ANG2 is ignored for a two-winding
            transformer. For a three-winding transformer, ANG2 is positive when the winding
            two bus voltage leads the T (or star) point bus voltage. ANG2 must be greater than
            -180.0o and less than or equal to +180.0o. ANG2 = 0.0 by default.
        RATA2, RATB2, RATC2: Winding 2’s three three-phase ratings, entered in either MVA or current expressed
            as MVA, according to the value specified for XFRRAT specified on the first data
            record (refer to Case Identification Data). RATA2 = 0.0, RATB2 = 0.0 and
            RATC2 = 0.0 (bypass loading limit check for this transformer winding) by default.
        COD2: The transformer control mode for automatic adjustments of the Winding 2 tap or
            phase shift angle during power flow solutions:
                0    for no control (fixed tap and fixed phase shift)
                ±1   for voltage control
                ±2   for reactive power flow control
                ±3   for active power flow control
                ±5   for asymmetric active power flow control
            If the control mode is entered as a positive number, automatic adjustment of this
            transformer winding is enabled when the corresponding adjustment is activated
            during power flow solutions; a negative control mode suppresses the automatic
            adjustment of this transformer winding. COD2 = 0 by default.
        CONT2:  The bus number, or extended bus name enclosed in single quotes (refer to
            Extended Bus Names), of the bus for which voltage is to be controlled by the trans-
            former turns ratio adjustment option of the power flow solution activities when
            COD2 is 1. CONT2 should be non-zero only for voltage controlling transformer
            windings.
            CONT2 may specify a bus other than I, J, or K; in this case, the sign of CONT2
            defines the location of the controlled bus relative to the transformer winding. If
            CONT2 is entered as a positive number, or a quoted extended bus name, the ratio
            is adjusted as if bus CONT2 is on the Winding 1 or Winding 3 side of the trans-
            former; if CONT2 is entered as a negative number, or a quoted extended bus name
            with a minus sign preceding the first character, the ratio is adjusted as if bus
            |CONT2| is on the Winding 2 side of the transformer. CONT2 = 0 by default.

        RMA2, RMI2:  When |COD2| is 1, 2 or 3, the upper and lower limits, respectively, of one of the
            following:
            • Off-nominal turns ratio in pu of Winding 2 bus base voltage when |COD2| is
            1 or 2 and CW is 1; RMA2 = 1.1 and RMI2 = 0.9 by default.
            • Actual Winding 2 voltage in kV when |COD2| is 1 or 2 and CW is 2. No default
            is allowed.
            • Off-nominal turns ratio in pu o f nominal Winding 2 voltage (NOMV2) when
            |COD2| is 1 or 2 and CW is 3; RMA2 = 1.1 and RMI2 = 0.9 by default.
            • Phase shift angle in degrees when |COD2| is 3. No default is allowed.
            Not used when |COD2| is 0; RMA2 = 1.1 and RMI2 = 0.9 by default.
        VMA2, VMI2:   When |COD2| is 1, 2 or 3, the upper and lower limits, respectively, of one of the
            following:
            • Voltage at the controlled bus (bus |CONT2|) in pu when |COD2| is 1.
            VMA2 = 1.1 and VMI2 = 0.9 by default.
            • Reactive power flow into the transformer at the Winding 2 bus end in Mvar
            when |COD2| is 2. No default is allowed.
            • Active power flow into the transformer at the Winding 2 bus end in MW when
            |COD2| is 3. No default is allowed.
            Not used when |COD2| is 0; VMA2 = 1.1 and VMI2 = 0.9 by default.
        NTP2 The number of tap positions available; used when COD2 is 1 or 2. NTP2 must be
            between 2 and 9999. NTP2 = 33 by default.
        TAB2 The number of a transformer impedance correction table if this transformer
            winding’s impedance is to be a function of either off-nominal turns ratio or phase
            shift angle (refer to Transformer Impedance Correction Tables), or 0 if no trans-
            former impedance correction is to be applied to this transformer winding. TAB2 = 0
            by default.
        CR2, CX2 The load drop compensation impedance for voltage controlling transformers
            entered in pu on system base quantities; used when COD2 is 1. CR2 + j CX2 = 0.0
            by default.
        CNXA2 Winding connection angle in degrees; used when COD2 is 5. There are no restrictions
            on the value specified for CNXA2; if it is outside of the range from -90.0 to
            +90.0, CNXA2 is normalized to within this range. CNXA2 = 0.0 by default.
            The fifth data record is specified only for three-winding transformers:
        WINDV3: When CW is 1, WINDV3 is the Winding 3 off-nominal turns ratio in pu of Winding 3
            bus base voltage; WINDV3 = 1.0 by default.
            When CW is 2, WINDV3 is the actual Winding 3 voltage in kV; WINDV3 is equal to
            the base voltage of bus K by default.
            When CW is 3, WINDV3 is the Winding 3 off-nominal turns ratio in pu of nominal
            Winding 3 voltage, NOMV3; WINDV3 = 1.0 by default.

        NOMV3 The nominal (rated) Winding 3 voltage base in kV, or zero to indicate that nominal
            Winding 3 voltage is assumed to be identical to the base voltage of bus K. NOMV3
            is used in converting tap ratio data between values in per unit of nominal Winding 3
            voltage and values in per unit of Winding 3 bus base voltage when CW is 3. NOMV3
            = 0.0 by default.
        ANG3 The winding three phase shift angle in degrees. ANG3 is positive when the winding
            three bus voltage leads the T (or star) point bus voltage. ANG3 must be greater
            than -180.0o and less than or equal to +180.0o. ANG3 = 0.0 by default.
        RATA3, RATB3, RATC3 Winding 3’s three three-phase ratings, entered in either MVA or current expressed
            as MVA, according to the value specified for XFRRAT specified on the first data
            record (refer to Case Identification Data). RATA3 = 0.0, RATB3 = 0.0 and
            RATC3 = 0.0 (bypass loading limit check for this transformer winding) by default.
        COD3 The transformer control mode for automatic adjustments of the Winding 3 tap or
            phase shift angle during power flow solutions:
            0    for no control (fixed tap and fixed phase shift)
            ±1   for voltage control
            ±2   for reactive power flow control
            ±3   for active power flow control
            ±5   for asymmetric active power flow control.

            If the control mode is entered as a positive number, automatic adjustment of this
            transformer winding is enabled when the corresponding adjustment is activated
            during power flow solutions; a negative control mode suppresses the automatic
            adjustment of this transformer winding. COD3 = 0 by default.
        CONT3:   The bus number, or extended bus name enclosed in single quotes (refer to
            Extended Bus Names), of the bus for which voltage is to be controlled by the trans-
            former turns ratio adjustment option of the power flow solution activities when
            COD3 is 1. CONT3 should be non-zero only for voltage controlling transformer
            windings.
            CONT3 may specify a bus other than I, J, or K; in this case, the sign of CONT3
            defines the location of the controlled bus relative to the transformer winding. If
            CONT3 is entered as a positive number, or a quoted extended bus name, the ratio
            is adjusted as if bus CONT3 is on the Winding 1 or Winding 2 side of the trans-
            former; if CONT3 is entered as a negative number, or a quoted extended bus name
            with a minus sign preceding the first character, the ratio is adjusted as if bus
            |CONT3| is on the Winding 3 side of the transformer. CONT3 = 0 by default.
        RMA3, RMI3:   When |COD3| is 1, 2 or 3, the upper and lower limits, respectively, of one of the
            following:
            • Off-nominal turns ratio in pu of Winding 3 bus base voltage when |COD3| is
            1 or 2 and CW is 1; RMA3 = 1.1 and RMI3 = 0.9 by default.
            • Actual Winding 3 voltage in kV when |COD3| is 1 or 2 and CW is 2. No default
            is allowed.
            • Off-nominal turns ratio in pu o f nominal Winding 3 voltage (NOMV3) when
            |COD3| is 1 or 2 and CW is 3; RMA3 = 1.1 and RMI3 = 0.9 by default.
            • Phase shift angle in degrees when |COD3| is 3. No default is allowed.
            Not used when |COD3| is 0; RMA3 = 1.1 and RMI3 = 0.9 by default.

        VMA3, VMI3:  When |COD3| is 1, 2 or 3, the upper and lower limits, respectively, of one of the
            following:
            • Voltage at the co ntrolled b us (bus |C ONT3|) in pu when |COD3| is 1.
            VMA3 = 1.1 and VMI3 = 0.9 by default.
            • Reactive power flow into the transformer at the Winding 3 bus end in Mvar
            when |COD3| is 2. No default is allowed.
            • Active power flow into the transformer at the Winding 3 bus end in MW when
            |COD3| is 3. No default is allowed.
            Not used when |COD3| is 0; VMA3 = 1.1 and VMI3 = 0.9 by default.
        NTP3 The number of tap positions available; used when COD3 is 1 or 2. NTP3 must be
            between 2 and 9999. NTP3 = 33 by default.
        TAB3 The number of a transformer impedance correction table if this transformer
            winding’s impedance is to be a function of either off-nominal turns ratio or phase
            shift angle (refer to Transformer Impedance Correction Tables), or 0 if no trans-
            former impedance correction is to be applied to this transformer winding. TAB3 = 0
            by default.
        CR3, CX3 The load drop compensation impedance for voltage controlling transformers
            entered in pu on system base quantities; used when COD3 is 1. CR3 + j CX3 = 0.0
            by default.
        CNXA3 Winding connection angle in degrees; used when COD3 is 5. There are no restrictions
            on the value specified for CNXA3; if it is outside of the range from -90.0 to
            +90.0, CNXA3 is normalized to within this range. CNXA3 = 0.0 by default.

        default.
            Args:
        data:
        version:
        """

        self.windings = 0
        self.O1 = ''
        self.F1 = ''
        self.O2 = ''
        self.F2 = ''
        self.O3 = ''
        self.F3 = ''
        self.O4 = ''
        self.F4 = ''
        var = [self.O1, self.F1, self.O2, self.F2, self.O3, self.F3, self.O4, self.F4]

        if version == 33:

            # Line 1: for both types

            self.I, self.J, self.K, self.CKT, self.CW, self.CZ, self.CM, self.MAG1, self.MAG2, self.NMETR, \
             self.NAME, self.STAT, *var, self.VECGRP = data[0]

            if len(data) == 4:
                self.windings = 2

                '''
                I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,’NAME’,STAT,O1,F1,...,O4,F4,VECGRP
                R1-2,X1-2,SBASE1-2
                WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD1,CONT1,RMA1,RMI1,VMA1,VMI1,NTP1,TAB1,CR1,CX1,CNXA1
                WINDV2,NOMV2
                '''

                self.R1_2, self.X1_2, self.SBASE1_2 = data[1]

                n = len(data[2])
                dta = np.zeros(17, dtype=object)
                dta[0:n] = data[2]

                self.WINDV1, self.NOMV1, self.ANG1, self.RATA1, self.RATB1, self.RATC1, self.COD1, self.CONT1, self.RMA1, \
                self.RMI1, self.VMA1, self.VMI1, self.NTP1, self.TAB1, self.CR1, self.CX1, self.CNXA1 = dta

                self.WINDV2, self.NOMV2 = data[3]

            else:
                self.windings = 3

                '''
                I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,’NAME’,STAT,O1,F1,...,O4,F4,VECGRP
                R1-2,X1-2,SBASE1-2,R2-3,X2-3,SBASE2-3,R3-1,X3-1,SBASE3-1,VMSTAR,ANSTAR
                WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD1,CONT1,RMA1,RMI1,VMA1,VMI1,NTP1,TAB1,CR1,CX1,CNXA1
                WINDV2,NOMV2,ANG2,RATA2,RATB2,RATC2,COD2,CONT2,RMA2,RMI2,VMA2,VMI2,NTP2,TAB2,CR2,CX2,CNXA2
                WINDV3,NOMV3,ANG3,RATA3,RATB3,RATC3,COD3,CONT3,RMA3,RMI3,VMA3,VMI3,NTP3,TAB3,CR3,CX3,CNXA3
                '''

                self.R1_2, self.X1_2, self.SBASE1_2, self.R2_3, self.X2_3, self.SBASE2_3, self.R3_1, self.X3_1, \
                self.SBASE3_1, self.VMSTAR, self.ANSTAR = data[1]

                self.WINDV1, self.NOMV1, self.ANG1, self.RATA1, self.RATB1, self.RATC1, self.COD1, self.CONT1, \
                self.RMA1, self.RMI1, self.VMA1, self.VMI1, self.NTP1, self.TAB1, self.CR1, self.CX1, self.CNXA1 = data[2]

                self.WINDV2, self.NOMV2, self.ANG2, self.RATA2, self.RATB2, self.RATC2, self.COD2, self.CONT2, \
                self.RMA2, self.RMI2, self.VMA2, self.VMI2, self.NTP2, self.TAB2, self.CR2, self.CX2, self.CNXA2 = data[3]

                self.WINDV3, self.NOMV3, self.ANG3, self.RATA3, self.RATB3, self.RATC3, self.COD3, self.CONT3, \
                self.RMA3, self.RMI3, self.VMA3, self.VMI3, self.NTP3, self.TAB3, self.CR3, self.CX3, self.CNXA3 = data[4]

        elif version == 32:

            '''
            I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,’NAME’,STAT,O1,F1,...,O4,F4

            R1-2,X1-2,SBASE1-2,R2-3,X2-3,SBASE2-3,R3-1,X3-1,SBASE3-1,VMSTAR,ANSTAR

            WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD1,CONT1,RMA1,RMI1,VMA1,VMI1,NTP1,TAB1,CR1,CX1,CNXA1

            WINDV2,NOMV2,ANG2,RATA2,RATB2,RATC2,COD2,CONT2,RMA2,RMI2,VMA2,VMI2,NTP2,TAB2,CR2,CX2,CNXA2
            WINDV3,NOMV3,ANG3,RATA3,RATB3,RATC3,COD3,CONT3,RMA3,RMI3,VMA3,VMI3,NTP3,TAB3,CR3,CX3,CNXA3
            '''

            # Line 1: for both types

            self.I, self.J, self.K, self.CKT, self.CW, self.CZ, self.CM, self.MAG1, self.MAG2, self.NMETR, \
             self.NAME, self.STAT, *var = data[0]

            if len(data[1]) == 3:
                # 2-windings
                self.windings = 2
                self.R1_2, self.X1_2, self.SBASE1_2 = data[1]
            else:
                # 3-windings
                self.windings = 3
                self.R1_2, self.X1_2, self.SBASE1_2, self.R2_3, self.X2_3, self.SBASE2_3, self.R3_1, \
                 self.X3_1, self.SBASE3_1, self.VMSTAR, self.ANSTAR = data[1]

            # line 3: for both types
            n = len(data[2])
            dta = np.zeros(17, dtype=object)
            dta[0:n] = data[2]
            self.WINDV1, self.NOMV1, self.ANG1, self.RATA1, self.RATB1, self.RATC1, self.COD1, self.CONT1, self.RMA1, \
             self.RMI1, self.VMA1, self.VMI1, self.NTP1, self.TAB1, self.CR1, self.CX1, self.CNXA1 = dta

            # line 4
            if len(data[3]) == 2:
                # 2-windings
                self.WINDV2, self.NOMV2 = data[3]
            else:
                # 3 - windings
                self.WINDV2, self.NOMV2, self.ANG2, self.RATA2, self.RATB2, self.RATC2, self.COD2, self.CONT2, \
                 self.RMA2, self.RMI2, self.VMA2, self.VMI2, self.NTP2, self.TAB2, self.CR2, self.CX2, self.CNXA2, \
                 self.WINDV3, self.NOMV3, self.ANG3, self.RATA3, self.RATB3, self.RATC3, self.COD3, self.CONT3, \
                 self.RMA3, self.RMI3, self.VMA3, self.VMI3, self.NTP3, self.TAB3, \
                 self.CR3, self.CX3, self.CNXA3 = data[3]

        elif version == 30:

            """
            I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,'NAME',STAT,Ol,Fl 04,F4

            R1—2,X1—2,SBASE1—2,R2—3,X2—3,SBASE2—3,R3—1,X3—1,SBASE3—1,VMSTAR,ANSTAR

            WINDV1,NOMV1,ANG1, RATA1, BATB1, RATC1, COD1, CONT1, RMA1, RMI1,VMA1,VMI1,NTP1, TAB1, CR1, CX1

            WINDV2 ,NOMV2 , ANG2 , RATA2 , BATB2 , RATC2, COD2, CONT2 , RMA2 , RMI2 , VMA2 , VMI2 ,NTP2, TAB2,CR2, CX2
            WINDV3,NOMV3,ANG3, RATA3, BATB3, RATC3, COD3, CONT3, RMA3, RMI3,VMA3,VMI3,NTP3, TAB3, CR3, CX3
            """

            self.I, self.J, self.K, self.CKT, self.CW, self.CZ, self.CM, self.MAG1, self.MAG2, self.NMETR, \
            self.NAME, self.STAT, *var = data[0]

            if len(data[1]) == 3:
                # 2-windings
                self.windings = 2
                self.R1_2, self.X1_2, self.SBASE1_2 = data[1]
            else:
                # 3-windings
                self.windings = 3
                self.R1_2, self.X1_2, self.SBASE1_2, self.R2_3, self.X2_3, self.SBASE2_3, self.R3_1, \
                self.X3_1, self.SBASE3_1, self.VMSTAR, self.ANSTAR = data[1]

            # line 3: for both types
            self.WINDV1, self.NOMV1, self.ANG1, self.RATA1, self.RATB1, self.RATC1, self.COD1, self.CONT1, self.RMA1, \
             self.RMI1, self.VMA1, self.VMI1, self.NTP1, self.TAB1, self.CR1, self.CX1 = data[2]

            # line 4
            if len(data[3]) == 2:
                # 2-windings
                self.WINDV2, self.NOMV2 = data[3]
            else:
                # 3 - windings
                self.WINDV2, self.NOMV2, self.ANG2, self.RATA2, self.RATB2, self.RATC2, self.COD2, self.CONT2, \
                 self.RMA2, self.RMI2, self.VMA2, self.VMI2, self.NTP2, self.TAB2, self.CR2, self.CX2, \
                 self.WINDV3, self.NOMV3, self.ANG3, self.RATA3, self.RATB3, self.RATC3, self.COD3, self.CONT3, \
                 self.RMA3, self.RMI3, self.VMA3, self.VMI3, self.NTP3, self.TAB3, \
                 self.CR3, self.CX3 = data[3]

        elif version == 29:

            '''
            In this version 
            
                2 windings -> 4 lines
                
                I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,’NAME’,STAT,O1,F1,...,O4,F4
                R1-2,X1-2,SBASE1-2
                WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD,CONT,RMA,RMI,VMA,VMI,NTP,TAB,CR,CX
                WINDV2,NOMV2
                
                3 windings -> 5 lines
                
                I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,’NAME’,STAT,O1,F1,...,O4,F4
                R1-2,X1-2,SBASE1-2,R2-3,X2-3,SBASE2-3,R3-1,X3-1,SBASE3-1,VMSTAR,ANSTAR
                WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD,CONT,RMA,RMI,VMA,VMI,NTP,TAB,CR,CX
                WINDV2,NOMV2,ANG2,RATA2,RATB2,RATC2
                WINDV3,NOMV3,ANG3,RATA3,RATB3,RATC3
                 
            '''

            self.I, self.J, self.K, self.CKT, self.CW, self.CZ, self.CM, self.MAG1, self.MAG2, self.NMETR, \
             self.NAME, self.STAT, *var = data[0]

            if len(data[1]) == 3:

                '''
                I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,’NAME’,STAT,O1,F1,...,O4,F4
                R1-2,X1-2,SBASE1-2
                WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD,CONT,RMA,RMI,VMA,VMI,NTP,TAB,CR,CX
                WINDV2,NOMV2
                '''

                # 2-windings
                self.windings = 2
                self.R1_2, self.X1_2, self.SBASE1_2 = data[1]

                self.WINDV1, self.NOMV1, self.ANG1, self.RATA1, self.RATB1, self.RATC1, self.COD1, self.CONT1, self.RMA1, \
                self.RMI1, self.VMA1, self.VMI1, self.NTP1, self.TAB1, self.CR1, self.CX1 = data[2]

                self.WINDV2, self.NOMV2 = data[3]

            else:

                '''
                I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,’NAME’,STAT,O1,F1,...,O4,F4
                R1-2,X1-2,SBASE1-2,R2-3,X2-3,SBASE2-3,R3-1,X3-1,SBASE3-1,VMSTAR,ANSTAR
                
                WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD,CONT,RMA,RMI,VMA,VMI,NTP,TAB,CR,CX
                
                WINDV2,NOMV2,ANG2,RATA2,RATB2,RATC2
                
                WINDV3,NOMV3,ANG3,RATA3,RATB3,RATC3
                '''

                # 3-windings
                self.windings = 3

                self.R1_2, self.X1_2, self.SBASE1_2, self.R2_3, self.X2_3, self.SBASE2_3, self.R3_1, \
                 self.X3_1, self.SBASE3_1, self.VMSTAR, self.ANSTAR = data[1]

                self.WINDV1, self.NOMV1, self.ANG1, self.RATA1, self.RATB1, self.RATC1, self.COD1, \
                 self.CONT1, self.RMA1,  self.RMI1, self.VMA1, self.VMI1, self.NTP1, self.TAB1, \
                 self.CR1, self.CX1 = data[2]

                self.WINDV2, self.NOMV2, self.ANG2, self.RATA2, self.RATB2, self.RATC2 = data[3]

                self.WINDV3, self.NOMV3, self.ANG3, self.RATA3, self.RATB3, self.RATC3 = data[4]

            pass

        else:
            logger.append('Transformer not implemented for version ' + str(version))

    def get_object(self, psse_bus_dict, logger: list):
        """
        Return GridCal branch object
        Args:
            psse_bus_dict: Dictionary that relates PSSe bus indices with GridCal Bus objects

        Returns:
            Gridcal Branch object
        """

        '''
        R1-2, X1-2 The measured impedance of the transformer between the buses to which its first
            and second windings are connected.
            
            When CZ is 1, they are the resistance and reactance, respectively, in pu on system
            MVA base and winding voltage base.
            
            When CZ is 2, they are the resistance and reactance, respectively, in pu on Winding
            1 to 2 MVA base (SBASE1-2) and winding voltage base.
            
            When CZ is 3, R1-2 is the load loss in watts, and X1-2 is the impedance magnitude
            in pu on Winding 1 to 2 MVA base (SBASE1-2) and winding voltage base. For
            three-phase transformers or three-phase banks of single phase transformers, R1-2
            should specify the three-phase load loss.
            
            R1-2 = 0.0 by default, but no default is allowed for X1-2.
        '''

        if self.windings == 2:
            bus_from = psse_bus_dict[self.I]
            bus_to = psse_bus_dict[self.J]

            name = str(self.I) + '_' + str(self.J) + '_' + str(self.CKT) + self.NAME.strip()
            name = name.replace("'", "")

            if self.CZ == 1:
                r = self.R1_2
                x = self.X1_2
                g = self.MAG1
                b = self.MAG2

            else:
                r = self.R1_2
                x = self.X1_2
                g = self.MAG1
                b = self.MAG2

                logger.append('Transformer impedance is not in p.u.')

            if self.CW == 1:
                tap_mod = self.WINDV1 * self.WINDV2
            else:
                tap_mod = 1.0

            elm = Branch(bus_from=bus_from, bus_to=bus_to,
                         name=name,
                         r=r,
                         x=x,
                         g=g,
                         b=b,
                         rate=max(self.RATA1, self.RATB1, self.RATC1),
                         tap=tap_mod,
                         shift_angle=self.ANG1,
                         active=bool(self.STAT),
                         mttf=0,
                         mttr=0,
                         branch_type=BranchType.Transformer)

            return [elm]

        elif self.windings == 3:

            bus_1 = psse_bus_dict[abs(self.I)]
            bus_2 = psse_bus_dict[abs(self.J)]
            bus_3 = psse_bus_dict[abs(self.K)]

            r = self.R1_2
            x = self.X1_2
            g = self.MAG1
            b = self.MAG2

            name1 = str(self.I) + '_' + str(self.J) + '_ij' + self.NAME.strip()
            name1 = name1.replace("'", "")

            object1 = Branch(bus_from=bus_1, bus_to=bus_2,
                             name=name1,
                             r=r,
                             x=x,
                             g=g,
                             b=b,
                             rate=max(self.RATA1, self.RATB1, self.RATC1),
                             tap=1,
                             shift_angle=0,
                             active=bool(self.STAT),
                             mttf=0,
                             mttr=0,
                             branch_type=BranchType.Transformer)

            r = self.R2_3
            x = self.X2_3
            g = self.MAG1
            b = self.MAG2

            name2 = str(self.J) + '_' + str(self.K) + '_jk' + self.NAME.strip()
            name2 = name2.replace("'", "")

            object2 = Branch(bus_from=bus_2, bus_to=bus_3,
                             name=name2,
                             r=r,
                             x=x,
                             g=g,
                             b=b,
                             rate=max(self.RATA1, self.RATB1, self.RATC1),
                             tap=1,
                             shift_angle=0,
                             active=bool(self.STAT),
                             mttf=0,
                             mttr=0,
                             branch_type=BranchType.Transformer)

            r = self.R3_1
            x = self.X3_1
            g = self.MAG1
            b = self.MAG2

            name3 = str(self.K) + '_' + str(self.I) + '_ki' + self.NAME.strip()
            name3 = name3.replace("'", "")

            object3 = Branch(bus_from=bus_3, bus_to=bus_1,
                             name=name3,
                             r=r,
                             x=x,
                             g=g,
                             b=b,
                             rate=max(self.RATA1, self.RATB1, self.RATC1),
                             tap=1,
                             shift_angle=0,
                             active=bool(self.STAT),
                             mttf=0,
                             mttr=0,
                             branch_type=BranchType.Transformer)

            return [object1, object2, object3]

        else:
            raise Exception(str(self.windings) + ' number of windings!')


class PSSeInterArea:

    def __init__(self, data, version, logger: list):
        """

        :param data:
        :param version:
        :param logger:
        """

        self.I = -1

        self.ARNAME = ''

        if version in [29, 30, 32, 33]:
            # I, ISW, PDES, PTOL, 'ARNAME'
            self.I, self.ISW, self.PDES, self.PTOL, self.ARNAME = data[0]

            self.ARNAME = self.ARNAME.replace("'", "").strip()
        else:
            logger.append('Areas not defined for version ' + str(version))


class PSSeArea:

    def __init__(self, data, version, logger: list):
        """

        :param data:
        :param version:
        :param logger:
        """

        self.I = -1

        self.ARNAME = ''

        if version in [29, 30, 32, 33]:
            # I, ISW, PDES, PTOL, 'ARNAME'
            self.I, self.ISW, self.PDES, self.PTOL, self.ARNAME = data[0]

            self.ARNAME = self.ARNAME.replace("'", "").strip()
        else:
            logger.append('Areas not defined for version ' + str(version))


class PSSeZone:

    def __init__(self, data, version, logger: list):
        """

        :param data:
        :param version:
        :param logger:
        """

        self.I = -1

        self.ZONAME = ''

        if version in [29, 30, 32, 33]:
            # I, 'ZONAME'
            self.I, self.ZONAME = data[0]

            self.ZONAME = self.ZONAME.replace("'", "").strip()
        else:
            logger.append('Zones not defined for version ' + str(version))


def interpret_line(line, splitter=','):
    """
    Split text into arguments and parse each of them to an appropriate format (int, float or string)
    Args:
        line:
        splitter:
    Returns: list of arguments
    """
    parsed = list()
    elms = line.split(splitter)

    for elm in elms:
        try:
            # try int
            el = int(elm)
        except Exception as ex1:
            try:
                # try float
                el = float(elm)
            except Exception as ex2:
                # otherwise just leave it as string
                el = elm.strip()
        parsed.append(el)
    return parsed


class PSSeParser:

    def __init__(self, file_name):
        """
        Parse PSSe file
        Args:
            file_name: file name or path
        """
        self.parsers = dict()
        self.versions = [33, 32, 30, 29]

        self.logger = Logger()

        self.file_name = file_name

        self.pss_grid, logs = self.parse_psse()

        self.logger += logs

        self.circuit = self.pss_grid.get_circuit(self.logger)

    def read_and_split(self):
        """
        Read the text file and split it into sections
        :return:
        """

        # make a guess of the file encoding
        detection = chardet.detect(open(self.file_name, "rb").read())

        # open the text file into a variable
        txt = ''
        with open(self.file_name, 'r', encoding=detection['encoding']) as my_file:
            for line in my_file:
                if line[0] != '@':
                    txt += line

        # split the text file into sections
        sections = txt.split(' /')

        sections_dict = dict()

        str_a = 'End of'.lower()
        str_b = 'data'.lower()

        for i, sec in enumerate(sections):
            data = sec.split('\n')
            first = data.pop(0).lower()
            if str_a in first:
                if ',' in first:
                    srch = first.split(',')[0]
                else:
                    srch = first
                name = re.search(str_a + '(.*)' + str_b, srch).group(1).strip()
                data2 = sections[i-1].split('\n')[1:]

                if name.lower() == 'bus':
                    data2.pop(0)
                    data2.pop(0)

                sections_dict[name] = data2

        return sections, sections_dict

    def parse_psse(self) -> (MultiCircuit, List[AnyStr]):
        """
        Parser implemented according to:
            - POM section 4.1.1 Power Flow Raw Data File Contents (v.29)
            - POM section 5.2.1                                   (v.33)
            - POM section 5.2.1                                   (v.32)

        Returns: MultiCircuit, List[str]
        """

        logger = Logger()

        sections, sections_dict = self.read_and_split()

        # header -> new grid
        grid = PSSeGrid(interpret_line(sections[0]))

        if grid.REV not in self.versions:
            logger.append('The PSSe version is not compatible. Compatible versions are:' + str(self.versions))
            return grid, logger
        else:
            version = grid.REV

        # declare contents:
        # section_idx, objects_list, expected_data_length, ObjectT, lines per objects

        # SEQUENCE ORDER:
        # 0:  Case Identification Data
        # 1:  Bus Data
        # 2:  Load Data
        # 3:  Fixed Bus Shunt Data
        # 4:  Generator Data
        # 5:  Non-Transformer Branch Data
        # 6:  Transformer Data
        # 7:  Area Interchange Data
        # 8:  Two-Terminal DC Transmission Line Data
        # 9:  Voltage Source Converter (VSC) DC Transmission Line Data
        # 10: Transformer Impedance Correction Tables
        # 11: Multi-Terminal DC Transmission Line Data
        # 12: Multi-Section Line Grouping Data
        # 13: Zone Data
        # 14: Inter-area Transfer Data
        # 15: Owner Data
        # 16: FACTS Device Data
        # 17: Switched Shunt Data
        # 18: GNE Device Data
        # 19: Induction Machine Data
        # 20: Q Record

        meta_data = dict()
        meta_data['bus'] = [grid.buses, PSSeBus, 1]
        meta_data['load'] = [grid.loads, PSSeLoad, 1]
        meta_data['fixed shunt'] = [grid.shunts, PSSeShunt, 1]
        meta_data['shunt'] = [grid.shunts, PSSeShunt, 1]
        meta_data['switched shunt'] = [grid.switched_shunts, PSSeSwitchedShunt, 1]
        meta_data['generator'] = [grid.generators, PSSeGenerator, 1]
        meta_data['induction machine'] = [grid.generators, PSSeInductionMachine, 3]
        meta_data['branch'] = [grid.branches, PSSeBranch, 1]
        meta_data['transformer'] = [grid.transformers, PSSeTransformer, 4]
        meta_data['two-terminal dc'] = [grid.branches, PSSeTwoTerminalDCLine, 3]
        meta_data['vsc dc line'] = [grid.branches, PSSeVscDCLine, 3]
        meta_data['area data'] = [grid.areas, PSSeArea, 1]
        meta_data['inter-area transfer'] = [grid.areas, PSSeInterArea, 1]
        meta_data['zone'] = [grid.zones, PSSeZone, 1]

        for key, values in meta_data.items():

            # get the parsers for the declared object type
            objects_list, ObjectT, lines_per_object = values

            if key in sections_dict.keys():
                lines = sections_dict[key]

                # iterate ove the object's lines to pack them as expected (normally 1 per object except transformers...)
                l = 0
                while l < len(lines):

                    lines_per_object2 = lines_per_object

                    if version in [29, 33] and key == 'transformer':
                        # as you know the PSS/e raw format is nuts, that is why for v29
                        # the transformers may have 4 or 5 lines to define them
                        if (l + 1) < len(lines):
                            dta = lines[l+1].split(',')
                            if len(dta) > 3:
                                # 3 - windings
                                lines_per_object2 = 5
                            else:
                                # 2-windings
                                lines_per_object2 = 4

                    if ',' in lines[l]:
                        data = list()
                        for k in range(lines_per_object2):
                            data.append(interpret_line(lines[l + k]))

                        # pick the line that matches the object and split it by line returns \n
                        # object_lines = line.split('\n')

                        # interpret each line of the object and store into data
                        # data is a vector of vectors with data definitions
                        # for the buses, branches, loads etc. data contains 1 vector,
                        # for the transformers data contains 4 vectors
                        # data = [interpret_line(object_lines[k]) for k in range(lines_per_object)]

                        # pass the data to the according object to assign it to the matching variables
                        objects_list.append(ObjectT(data, version, logger))

                    else:
                        logger.append('Skipped:' + lines[l])

                    # add lines
                    l += lines_per_object2

            else:
                logger.append('"' + key + '" is not in the data')

        # add logs for the non parsed objects
        for key in sections_dict.keys():
            if key not in meta_data.keys():
                logger.append(key + ' is not implemented in the parser.')

        return grid, logger


if __name__ == '__main__':

    fname = '/home/santi/Descargas/PSS_file.raw'

    pss_parser = PSSeParser(fname)

    print()

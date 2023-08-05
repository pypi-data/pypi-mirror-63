import os
import string
import sys
from enum import Enum
import PySide2

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math

from PySide2.QtWidgets import *

from GridCal.Gui.Analysis.gui import *
from GridCal.Engine.Core.multi_circuit import MultiCircuit
from GridCal.Engine.Devices import *


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a Qt table view with a pandas data frame
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = np.array(data.values)
        self._cols = data.columns
        self.index = data.index.values
        self.r, self.c = np.shape(self._data)
        self.isDate = False
        if isinstance(self.index[0], np.datetime64):
            self.index = pd.to_datetime(self.index)
            self.isDate = True

        self.formatter = lambda x: "%.2f" % x

    def rowCount(self, parent=None):
        return self.r

    def columnCount(self, parent=None):
        return self.c

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data[index.row(), index.column()])
        return None

    def headerData(self, p_int, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._cols[p_int]
            elif orientation == QtCore.Qt.Vertical:
                if self.index is None:
                    return p_int
                else:
                    if self.isDate:
                        return self.index[p_int].strftime('%Y/%m/%d  %H:%M.%S')
                    else:
                        return str(self.index[p_int])
        return None


def get_list_model(iterable):
    """
    get Qt list model from a simple iterable
    :param iterable: 
    :return: List model
    """
    list_model = QtGui.QStandardItemModel()
    if iterable is not None:
        for val in iterable:
            # for the list model
            item = QtGui.QStandardItem(val)
            item.setEditable(False)
            list_model.appendRow(item)
    return list_model


class GridErrorLog:

    def __init__(self, parent=None):

        self.logs = dict()

        self.header = ['Object type', 'Name', 'Index', 'Severity', 'Property']

    def add(self, object_type, element_name, element_index, severity, propty, message):
        """

        :param object_type:
        :param element_name:
        :param element_index:
        :param severity:
        :param propty:
        :param message:
        :return:
        """

        e = [object_type, element_name, element_index, severity, propty]

        if message in self.logs.keys():
            self.logs[message].append(e)
        else:
            self.logs[message] = [e]

    def clear(self):
        """
        Delete all logs
        """
        self.logs = list()

    def get_model(self) -> "QtGui.QStandardItemModel":
        """
        Get TreeView Model
        :return: QStandardItemModel
        """
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(self.header)

        # populate data
        for message_key, entries in self.logs.items():
            parent1 = QtGui.QStandardItem(message_key)
            for object_type, element_name, element_index, severity, prop in entries:

                parent1.appendRow([QtGui.QStandardItem(str(object_type)),
                                   QtGui.QStandardItem(str(element_name)),
                                   QtGui.QStandardItem(str(element_index)),
                                   QtGui.QStandardItem(str(severity)),
                                   QtGui.QStandardItem(str(prop))])
            model.appendRow(parent1)

        return model


class GridAnalysisGUI(QtWidgets.QDialog):

    def __init__(self, parent=None, object_types=list(), circuit: MultiCircuit=None):
        """
        Constructor
        Args:
            parent:
            object_types:
            circuit:
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Grid analysis')

        # set the circuit
        self.circuit = circuit

        # declare logs
        self.log = GridErrorLog()

        self.object_types = object_types

        # set the objects type model
        self.ui.objectsListView.setModel(get_list_model(object_types))

        # click
        # self.ui.doit_button.clicked.connect(self.analyze_click)

        # list click
        self.ui.objectsListView.clicked.connect(self.object_type_selected)

        # Actions
        self.ui.plotwidget.canvas.fig.clear()
        self.ui.plotwidget.get_figure().set_facecolor('white')
        self.ui.plotwidget.get_axis().set_facecolor('white')

        self.analyze_all()

    def msg(self, text, title="Warning"):
        """
        Message box
        :param text: Text to display
        :param title: Name of the window
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle(title)
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def plot_analysis(self, object_type, fig=None):
        """
        PLot data + histogram
        Args:
            object_type:
            fig:
        """

        if object_type == 'branches':
            properties = ['R', 'X', 'G', 'B', 'rate']
            types = [float, float, float, float, float]
            log_scale = [False, False, False, False, False]
            objects = self.circuit.branches

        elif object_type == 'buses':
            properties = ['Vnom']
            types = [float]
            log_scale = [False]
            objects = self.circuit.buses

        elif object_type == 'generators':
            properties = ['Vset', 'P', 'Qmin', 'Qmax']
            log_scale = [False, False, False, False]
            types = [float, float, float, float]
            objects = self.circuit.get_generators()

        elif object_type == 'batteries':
            properties = ['Vset', 'P', 'Qmin', 'Qmax']
            log_scale = [False, False, False, False]
            types = [float, float, float, float]
            objects = self.circuit.get_batteries()

        elif object_type == 'static generators':
            properties = ['P', 'Q']
            log_scale = [False, False]
            types = [float, float]
            objects = self.circuit.get_static_generators()

        elif object_type == 'shunts':
            properties = ['G', 'B']
            log_scale = [False, False]
            types = [float, float]
            objects = self.circuit.get_shunts()

        elif object_type == 'loads':
            properties = ['P', 'Q', 'Ir', 'Ii', 'G', 'B']
            log_scale = [False, False, False, False, False, False]
            types = [float, float, float, float, float, float]
            objects = self.circuit.get_loads()

        else:
            return

        # fill values
        p = 0
        for i in range(len(properties)):
            if types[i] is complex:
                p += 2
            else:
                p += 1

        n = len(objects)
        vals = np.zeros((n, p))
        extended_prop = [None] * p
        log_scale_extended = [None] * p
        for i, elem in enumerate(objects):
            a = 0
            for j in range(len(properties)):
                if types[j] is complex:
                    val = getattr(elem, properties[j])
                    vals[i, a] = val.real
                    vals[i, a + 1] = val.imag
                    extended_prop[a] = properties[j] + '.re'
                    extended_prop[a + 1] = properties[j] + '.im'
                    log_scale_extended[a] = log_scale[j]
                    log_scale_extended[a + 1] = log_scale[j]
                    a += 2
                else:
                    vals[i, a] = getattr(elem, properties[j])
                    extended_prop[a] = properties[j]
                    log_scale_extended[a] = log_scale[j]
                    a += 1

        # create figure if needed
        if fig is None:
            fig = plt.figure(figsize=(12, 6))
        fig.suptitle('Analysis of the ' + object_type, fontsize=16)
        fig.set_facecolor('white')

        if n > 0:
            k = int(math.sqrt(p))
            axs = [None] * p

            for j in range(p):
                x = vals[:, j]
                mu = x.mean()
                variance = x.var()
                sigma = math.sqrt(variance)
                r = (mu - 6 * sigma, mu + 6 * sigma)

                # print checks
                l = np.where(x < r[0])[0]
                u = np.where(x > r[1])[0]

                print(extended_prop[j], r, '\n\t', l, '\n\t', u)

                # plot
                axs[j] = fig.add_subplot(k, k + 1, j + 1)
                axs[j].set_facecolor('white')
                axs[j].hist(x, bins=100, range=r,
                            cumulative=False, bottom=None, histtype='bar',
                            align='mid', orientation='vertical')
                axs[j].plot(x, np.zeros(n), 'o')
                axs[j].set_title(extended_prop[j])

                if log_scale_extended[j]:
                    axs[j].set_xscale('log')

    def object_type_selected(self):
        """
        On click-plot
        Returns:

        """
        if len(self.ui.objectsListView.selectedIndexes()) > 0:
            obj_type = self.ui.objectsListView.selectedIndexes()[0].data().lower()  # selected text
            self.ui.plotwidget.canvas.fig.clear()
            self.plot_analysis(object_type=obj_type, fig=self.ui.plotwidget.get_figure())
            self.ui.plotwidget.redraw()
        else:
            self.msg('Select a data structure')

    def analyze_all(self, imbalance_threshold=0.1, v_low=0.95, v_high=1.05):
        """
        Analyze the model data
        :param imbalance_threshold: Allowed percentage of imbalance
        :param v_low: lower voltage setting
        :param v_high: higher voltage setting
        :param format_str: Formatting string
        :return:
        """

        Pl = 0
        Pg = 0
        Pl_prof = 0
        Pg_prof = 0

        Ql = 0
        Qg = 0
        Ql_prof = 0
        Qg_prof = 0

        print('Analyzing...')
        # declare logs
        self.log = GridErrorLog()

        for object_type in self.object_types:

            if object_type.lower() == 'branches':
                elements = self.circuit.branches
                for i, elm in enumerate(elements):

                    if elm.branch_type != BranchType.Transformer:
                        V1 = min(elm.bus_to.Vnom, elm.bus_from.Vnom)
                        V2 = max(elm.bus_to.Vnom, elm.bus_from.Vnom)

                        s = '[' + str(V1) + '-' + str(V2) + ']'

                        if V1 > 0 and V2 > 0:
                            per = V1 / V2
                            if per < 0.9:
                                self.log.add(object_type='Branch', element_name=elm.name, element_index=i,
                                             severity='High',
                                             propty='Connection',
                                             message='The branch is connected between voltages '
                                                      'that differ in 10% or more. Should this be a transformer?' + s)
                        else:
                            self.log.add(object_type='Branch', element_name=elm.name, element_index=i, severity='High',
                                         propty='Voltage', message='The branch does is connected to a bus with '
                                                                   'Vnom=0, this is terrible.' + s)

                    if elm.name == '':
                        self.log.add(object_type='Branch', element_name=elm.name, element_index=i, severity='High',
                                     propty='name', message='The branch does not have a name')

                    if elm.rate <= 0.0:
                        self.log.add(object_type='Branch', element_name=elm.name, element_index=i, severity='High',
                                     propty='rate', message='There is no nominal power')

                    if elm.R == 0.0 and elm.X == 0.0:
                        self.log.add(object_type='Branch', element_name=elm.name, element_index=i, severity='High',
                                     propty='R+X', message='There is no impedance, set at least a very low value')

                    else:
                        if elm.R < 0.0:
                            self.log.add(object_type='Branch', element_name=elm.name, element_index=i,
                                         severity='Medium',
                                         propty='R', message='The resistance is negative, that cannot be.')
                        elif elm.R == 0.0:
                            self.log.add(object_type='Branch', element_name=elm.name, element_index=i,
                                         severity='Low',
                                         propty='R', message='The resistance is exactly zero')
                        elif elm.X == 0.0:
                            self.log.add(object_type='Branch', element_name=elm.name, element_index=i,
                                         severity='Low',
                                         propty='X', message='The reactance is exactly zero')

            elif object_type.lower() == 'buses':
                elements = self.circuit.buses
                names = set()

                for i, elm in enumerate(elements):

                    if elm.Vnom <= 0.0:
                        self.log.add(object_type='Bus', element_name=elm.name, element_index=i, severity='High',
                                     propty='Vnom', message='The nominal voltage is <= 0, this causes problems')

                    if elm.name == '':
                        self.log.add(object_type='Bus', element_name=elm.name, element_index=i, severity='High',
                                     propty='name', message='The bus does not have a name')

                    if elm.name in names:
                        self.log.add(object_type='Bus', element_name=elm.name, element_index=i, severity='High',
                                     propty='name', message='The bus name is not unique')

                    # add the name to a set
                    names.add(elm.name)

            elif object_type.lower() == 'generators':

                elements = self.circuit.get_generators()

                for k, obj in enumerate(elements):
                    Pg += obj.P

                    if self.circuit.time_profile is not None:
                        Pg_prof += obj.P_prof

                    if obj.Vset < v_low:
                        self.log.add(object_type='Generator',
                                     element_name=obj,
                                     element_index=k,
                                     severity='Medium',
                                     propty='Vset=' + str(obj.Vset) + '<' + str(v_low),
                                     message='The set point looks too low')
                    elif obj.Vset > v_high:
                        self.log.add(object_type='Generator',
                                     element_name=obj,
                                     element_index=k,
                                     severity='Medium',
                                     propty='Vset=' + str(obj.Vset) + '>' + str(v_high),
                                     message='The set point looks too high')

            elif object_type.lower() == 'batteries':
                elements = self.circuit.get_batteries()

                for obj in elements:
                    Pg += obj.P

                    if self.circuit.time_profile is not None:
                        Pg_prof += obj.P_prof

            elif object_type.lower() == 'static generators':
                elements = self.circuit.get_static_generators()

                for k, obj in enumerate(elements):
                    Pg += obj.P
                    Qg += obj.Q

                    if self.circuit.time_profile is not None:
                        Pg_prof += obj.P_prof
                        Qg_prof += obj.Q_prof

            elif object_type.lower() == 'shunts':
                elements = self.circuit.get_shunts()

            elif object_type.lower() == 'loads':
                elements = self.circuit.get_loads()

                for obj in elements:
                    Pl += obj.P
                    Ql += obj.Q

                    if self.circuit.time_profile is not None:
                        Pl_prof += obj.P_prof
                        Ql_prof += obj.Q_prof

        # compare loads
        p_ratio = abs(Pl - Pg) / (Pl + 1e-20)

        if p_ratio > imbalance_threshold:
            msg = "{:.1f}".format(p_ratio * 100) + "% >> " + str(imbalance_threshold) + "%"
            self.log.add(object_type='Grid snapshot',
                         element_name=self.circuit,
                         element_index=-1,
                         severity='High',
                         propty='Active power balance ' + msg,
                         message='There is too much active power imbalance')

        if self.circuit.time_profile is not None:
            nt = len(self.circuit.time_profile)
            for t in range(nt):
                p_ratio = abs(Pl_prof[t] - Pg_prof[t]) / (Pl_prof[t] + 1e-20)
                if p_ratio > imbalance_threshold:
                    msg = "{:.1f}".format(p_ratio * 100) + "% >> " + str(imbalance_threshold) + "%"
                    self.log.add(object_type='Grid time events',
                                 element_name=self.circuit,
                                 element_index=t,
                                 severity='High',
                                 propty='Active power balance ' + msg,
                                 message='There is too much active power imbalance')

        # set logs
        self.ui.logsTreeView.setModel(self.log.get_model())
        print('Done!')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = GridAnalysisGUI()
    window.resize(1.61 * 700.0, 700.0)  # golden ratio
    window.show()
    sys.exit(app.exec_())


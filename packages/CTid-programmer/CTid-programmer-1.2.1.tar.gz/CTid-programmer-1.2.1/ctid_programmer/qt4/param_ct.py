# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctid_programmer/qt4/param_ct.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Param_CT(object):
    def setupUi(self, Param_CT):
        Param_CT.setObjectName(_fromUtf8("Param_CT"))
        Param_CT.resize(387, 550)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_CT.sizePolicy().hasHeightForWidth())
        Param_CT.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Param_CT)
        self.verticalLayout.setContentsMargins(-1, 24, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_9 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.current_spinbox = QtGui.QDoubleSpinBox(Param_CT)
        self.current_spinbox.setDecimals(1)
        self.current_spinbox.setMaximum(6553.5)
        self.current_spinbox.setObjectName(_fromUtf8("current_spinbox"))
        self.gridLayout.addWidget(self.current_spinbox, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.size_spinbox = QtGui.QDoubleSpinBox(Param_CT)
        self.size_spinbox.setDecimals(1)
        self.size_spinbox.setMaximum(6553.5)
        self.size_spinbox.setObjectName(_fromUtf8("size_spinbox"))
        self.gridLayout.addWidget(self.size_spinbox, 1, 1, 1, 1)
        self.label_10 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.output_voltage_spinbox = QtGui.QDoubleSpinBox(Param_CT)
        self.output_voltage_spinbox.setDecimals(5)
        self.output_voltage_spinbox.setMaximum(0.65535)
        self.output_voltage_spinbox.setSingleStep(0.001)
        self.output_voltage_spinbox.setObjectName(_fromUtf8("output_voltage_spinbox"))
        self.gridLayout.addWidget(self.output_voltage_spinbox, 2, 1, 1, 1)
        self.label_23 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout.addWidget(self.label_23, 3, 0, 1, 1)
        self.phase_spinbox = QtGui.QDoubleSpinBox(Param_CT)
        self.phase_spinbox.setMinimum(-20.48)
        self.phase_spinbox.setMaximum(20.47)
        self.phase_spinbox.setObjectName(_fromUtf8("phase_spinbox"))
        self.gridLayout.addWidget(self.phase_spinbox, 3, 1, 1, 1)
        self.label_11 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.voltage_temp_coeff_spinbox = QtGui.QDoubleSpinBox(Param_CT)
        self.voltage_temp_coeff_spinbox.setDecimals(0)
        self.voltage_temp_coeff_spinbox.setMinimum(-640.0)
        self.voltage_temp_coeff_spinbox.setMaximum(635.0)
        self.voltage_temp_coeff_spinbox.setSingleStep(5.0)
        self.voltage_temp_coeff_spinbox.setObjectName(_fromUtf8("voltage_temp_coeff_spinbox"))
        self.gridLayout.addWidget(self.voltage_temp_coeff_spinbox, 4, 1, 1, 1)
        self.label_12 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)
        self.phase_temp_coeff_spinbox = QtGui.QDoubleSpinBox(Param_CT)
        self.phase_temp_coeff_spinbox.setObjectName(_fromUtf8("phase_temp_coeff_spinbox"))
        self.gridLayout.addWidget(self.phase_temp_coeff_spinbox, 5, 1, 1, 1)
        self.label_13 = QtGui.QLabel(Param_CT)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 6, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.params = QtGui.QGridLayout()
        self.params.setObjectName(_fromUtf8("params"))
        self.label_14 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.params.addWidget(self.label_14, 1, 1, 1, 1)
        self.calv3 = QtGui.QDoubleSpinBox(Param_CT)
        self.calv3.setMinimum(-2.56)
        self.calv3.setMaximum(2.54)
        self.calv3.setSingleStep(0.02)
        self.calv3.setObjectName(_fromUtf8("calv3"))
        self.params.addWidget(self.calv3, 3, 2, 1, 1)
        self.label_17 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.params.addWidget(self.label_17, 4, 1, 1, 1)
        self.calp3 = QtGui.QDoubleSpinBox(Param_CT)
        self.calp3.setMinimum(-2.56)
        self.calp3.setMaximum(2.54)
        self.calp3.setSingleStep(0.02)
        self.calp3.setObjectName(_fromUtf8("calp3"))
        self.params.addWidget(self.calp3, 3, 3, 1, 1)
        self.calv2 = QtGui.QDoubleSpinBox(Param_CT)
        self.calv2.setMinimum(-2.56)
        self.calv2.setMaximum(2.54)
        self.calv2.setSingleStep(0.02)
        self.calv2.setObjectName(_fromUtf8("calv2"))
        self.params.addWidget(self.calv2, 2, 2, 1, 1)
        self.calv1 = QtGui.QDoubleSpinBox(Param_CT)
        self.calv1.setMinimum(-2.56)
        self.calv1.setMaximum(2.54)
        self.calv1.setSingleStep(0.02)
        self.calv1.setObjectName(_fromUtf8("calv1"))
        self.params.addWidget(self.calv1, 1, 2, 1, 1)
        self.calp2 = QtGui.QDoubleSpinBox(Param_CT)
        self.calp2.setMinimum(-2.56)
        self.calp2.setMaximum(2.54)
        self.calp2.setSingleStep(0.02)
        self.calp2.setObjectName(_fromUtf8("calp2"))
        self.params.addWidget(self.calp2, 2, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.params.addItem(spacerItem, 2, 0, 1, 1)
        self.label_16 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.params.addWidget(self.label_16, 3, 1, 1, 1)
        self.label_15 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.params.addWidget(self.label_15, 2, 1, 1, 1)
        self.calp4 = QtGui.QDoubleSpinBox(Param_CT)
        self.calp4.setMinimum(-2.56)
        self.calp4.setMaximum(2.54)
        self.calp4.setSingleStep(0.02)
        self.calp4.setObjectName(_fromUtf8("calp4"))
        self.params.addWidget(self.calp4, 4, 3, 1, 1)
        self.label_20 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.params.addWidget(self.label_20, 0, 1, 1, 1)
        self.calp1 = QtGui.QDoubleSpinBox(Param_CT)
        self.calp1.setMinimum(-2.56)
        self.calp1.setMaximum(2.54)
        self.calp1.setSingleStep(0.02)
        self.calp1.setObjectName(_fromUtf8("calp1"))
        self.params.addWidget(self.calp1, 1, 3, 1, 1)
        self.calv4 = QtGui.QDoubleSpinBox(Param_CT)
        self.calv4.setMinimum(-2.56)
        self.calv4.setMaximum(2.54)
        self.calv4.setSingleStep(0.02)
        self.calv4.setObjectName(_fromUtf8("calv4"))
        self.params.addWidget(self.calv4, 4, 2, 1, 1)
        self.label_18 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.params.addWidget(self.label_18, 0, 2, 1, 1)
        self.label_19 = QtGui.QLabel(Param_CT)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.params.addWidget(self.label_19, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.params)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Param_CT)
        QtCore.QMetaObject.connectSlotsByName(Param_CT)
        Param_CT.setTabOrder(self.current_spinbox, self.size_spinbox)
        Param_CT.setTabOrder(self.size_spinbox, self.output_voltage_spinbox)
        Param_CT.setTabOrder(self.output_voltage_spinbox, self.phase_spinbox)
        Param_CT.setTabOrder(self.phase_spinbox, self.voltage_temp_coeff_spinbox)
        Param_CT.setTabOrder(self.voltage_temp_coeff_spinbox, self.phase_temp_coeff_spinbox)
        Param_CT.setTabOrder(self.phase_temp_coeff_spinbox, self.calv1)
        Param_CT.setTabOrder(self.calv1, self.calp1)
        Param_CT.setTabOrder(self.calp1, self.calv2)
        Param_CT.setTabOrder(self.calv2, self.calp2)
        Param_CT.setTabOrder(self.calp2, self.calv3)
        Param_CT.setTabOrder(self.calv3, self.calp3)
        Param_CT.setTabOrder(self.calp3, self.calv4)
        Param_CT.setTabOrder(self.calv4, self.calp4)

    def retranslateUi(self, Param_CT):
        self.label_9.setText(_translate("Param_CT", "Rated Current", None))
        self.current_spinbox.setSuffix(_translate("Param_CT", " A", None))
        self.label_5.setText(_translate("Param_CT", "Size", None))
        self.size_spinbox.setSuffix(_translate("Param_CT", " mm", None))
        self.label_10.setText(_translate("Param_CT", "Output Voltage at Rated Current", None))
        self.output_voltage_spinbox.setSuffix(_translate("Param_CT", " V", None))
        self.label_23.setText(_translate("Param_CT", "Output Phase at Rated Current", None))
        self.phase_spinbox.setSuffix(_translate("Param_CT", " °", None))
        self.label_11.setText(_translate("Param_CT", "Voltage Temperature Coefficient", None))
        self.voltage_temp_coeff_spinbox.setSuffix(_translate("Param_CT", " ppm/°C", None))
        self.label_12.setText(_translate("Param_CT", "Phase Temperature Coefficient", None))
        self.phase_temp_coeff_spinbox.setSuffix(_translate("Param_CT", " ppm/°C", None))
        self.label_13.setText(_translate("Param_CT", "Calibration Table", None))
        self.label_14.setText(_translate("Param_CT", "1.5%", None))
        self.calv3.setSuffix(_translate("Param_CT", " %", None))
        self.label_17.setText(_translate("Param_CT", "50%", None))
        self.calp3.setSuffix(_translate("Param_CT", " °", None))
        self.calv2.setSuffix(_translate("Param_CT", " %", None))
        self.calv1.setSuffix(_translate("Param_CT", " %", None))
        self.calp2.setSuffix(_translate("Param_CT", " °", None))
        self.label_16.setText(_translate("Param_CT", "15%", None))
        self.label_15.setText(_translate("Param_CT", "5%", None))
        self.calp4.setSuffix(_translate("Param_CT", " °", None))
        self.label_20.setText(_translate("Param_CT", "Level", None))
        self.calp1.setSuffix(_translate("Param_CT", " °", None))
        self.calv4.setSuffix(_translate("Param_CT", " %", None))
        self.label_18.setText(_translate("Param_CT", "Voltage Adjustment", None))
        self.label_19.setText(_translate("Param_CT", "Phase Adjustment", None))


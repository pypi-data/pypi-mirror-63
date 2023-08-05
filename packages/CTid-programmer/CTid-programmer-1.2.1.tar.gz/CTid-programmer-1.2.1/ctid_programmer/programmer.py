#!/usr/bin/env python3
#
# Copyright (c) 2016-2017, 2019-2020 eGauge Systems LLC
# 	1644 Conestoga St, Suite 2
# 	Boulder, CO 80301
# 	voice: 720-545-9767
# 	email: davidm@egauge.net
#
#  All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import argparse
import logging
import os
import sys
import tempfile

import pexpect
import pkg_resources

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction, QApplication, QDialog, QMainWindow, \
    QMessageBox, QListWidgetItem

import egauge.ctid as ctid

from egauge.qt4 import terminal

from ctid_programmer import preferences
from ctid_programmer import sensor_params
from ctid_programmer import sn
from ctid_programmer import sn_egauge
from ctid_programmer import sn_local
from ctid_programmer import template

from ctid_programmer.qt4.main_window import Ui_MainWindow
from ctid_programmer.qt4.template_dialog import Ui_Template_Dialog
from ctid_programmer.qt4.preferences_dialog import Ui_Preferences_Dialog
from ctid_programmer.qt4.param_ct import Ui_Param_CT
from ctid_programmer.qt4.param_volt import Ui_Param_Volt
from ctid_programmer.qt4.param_temp import Ui_Param_Temp
from ctid_programmer.qt4.param_ntc import Ui_Param_NTC
from ctid_programmer.qt4.param_pulse import Ui_Param_Pulse

PATH_AVRDUDE = 'avrdude'
PATH_CTID_ENCODER = 'ctid-encoder'

PATH_RESOURCES = pkg_resources \
                 .resource_filename(__name__,
                                    'lib/CTid-programmer/resources')
PATH_CODE_DIR = pkg_resources.resource_filename(__name__, 'resources/code')
PATH_ICON_DIR = os.path.join(PATH_RESOURCES, 'icons')
PATH_STATE_DIR = os.path.join(os.getenv('HOME'), '.CTid')

SENSOR_LONG_NAME = {
    'AC': 'AC Current Sensor',
    'DC': 'DC Current Sensor',
    'RC': 'Rogowski Coil Sensor',
    'voltage': 'Voltage Sensor',
    'temp': 'Linear Temperature Sensor',
    'NTC': 'NTC Thermistor Sensor',
    'pulse': 'Pulse Sensor'
}

# Filename of template to use for each sensor-type:
CODE_TEMPLATE = {
    'AC': 'ac.hex',
    'RC': 'ac.hex'
}

CHIP_ID_TO_NAME = {
    0x1e9008: ('t9', 'ATtiny9'),
    0x1e9003: ('t10', 'ATtiny10')
}

class Command_Processor:
    def __init__(self, argv, pattern_list=None, logfile=None):
        self.pattern_list = pattern_list + [pexpect.EOF, pexpect.TIMEOUT]
        self.error = None
        self.exit_status = None
        self.prog = None

        try:
            self.prog = pexpect.spawn(argv[0], argv[1:],
                                      encoding='utf-8', codec_errors='replace',
                                      logfile=logfile)
        except pexpect.ExceptionPexpect:
            self.error = 'Failed to start command: %s' % sys.exc_info()[1]
            return

    def __iter__(self):
        return self

    def __next__(self):
        while self.prog is not None:
            got = self.prog.expect(self.pattern_list, timeout=0.1)
            if got < len(self.pattern_list) - 2:
                return (got, self.prog.match)
            if got == len(self.pattern_list) - 2:
                self.prog.close()
                self.exit_status = self.prog.exitstatus
                break   # EOF: done
            if got == len(self.pattern_list) - 1:
                pass    # timeout; process events and then try again...
            QApplication.processEvents()
        raise StopIteration

    def stop(self):
        if self.error is None:
            self.error = 'program interrupted by user'
        self.prog.close()
        self.prog = None

class Template_List_Dialog(QDialog, Ui_Template_Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.listWidget.itemChanged.connect(self.item_changed)
        self.listWidget.itemDoubleClicked.connect(self.item_double_clicked)
        self.operation = None

        action = QAction('Rename', self)
        action.triggered.connect(self.rename_selected_template)
        self.listWidget.addAction(action)

        action = QAction('Delete', self)
        action.triggered.connect(self.delete_selected_template)
        self.listWidget.addAction(action)

        template_names = []
        for name, _ in self.parent.template_manager.items():
            template_names.append(name)
        template_names.sort()
        for name in template_names:
            self.add_template(name)

    def add_template(self, name):
        item = QListWidgetItem(name, self.listWidget)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        # save a copy of the original name as user data for renames:
        item.setData(Qt.UserRole, name)

    def rename_selected_template(self, is_checked):
        #pylint: disable=unused-argument
        self.listWidget.editItem(self.listWidget.currentItem())

    def delete_selected_template(self, is_checked):
        #pylint: disable=unused-argument
        item = self.listWidget.currentItem()
        self.parent.template_manager.remove(item.text())

        idx = self.listWidget.row(item)
        self.listWidget.takeItem(idx)

    def item_double_clicked(self):
        if self.operation == 'save':
            self.lineEdit.setText(self.listWidget.currentItem().text())
        self.accept()

    def item_changed(self):
        item = self.listWidget.currentItem()
        if item is None:
            return
        new_name = item.text()
        old_name = item.data(Qt.UserRole)
        if new_name != old_name:
            template = self.parent.template_manager.load(old_name)
            self.parent.template_manager.save(template, new_name)
            self.parent.template_manager.remove(old_name)

    def accept(self):
        if self.operation == 'save':
            new_name = self.lineEdit.text().strip().lstrip()
            if not new_name:
                QMessageBox.warning(self, 'Template Name Missing',
                                    'Please enter a template name.',
                                    QMessageBox.Ok)
                self.lineEdit.setFocus()
                self.lineEdit.selectAll()
                return
            if new_name in dict(self.parent.template_manager.items()):
                choice = QMessageBox.question(self,
                                              'Template Name Exists',
                                              'A template named `%s\' '
                                              'exists already.  '
                                              'Would you like to replace '
                                              'that template?' % new_name,
                                              'Replace', 'Cancel')
                if choice == 1:
                    return	# let user correct name
            else:
                self.add_template(new_name)
            template = self.parent.get_template()
            self.parent.template_manager.save(template, new_name)
        else:
            item = self.listWidget.currentItem()
            name = item.text()
            template = self.parent.template_manager.load(name)
            self.parent.template_activate(template)
            self.parent.log('Template `%s\' loaded.' % name)

        super().accept()

class Preferences_Editor(QDialog, Ui_Preferences_Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)

    def exec(self):
        self.sn_service_combo.currentIndexChanged.connect(
            self.sn_service_changed)
        self.sn_service_combo.setCurrentIndex(0)
        selected_service = self.parent.preferences.sn_service
        if selected_service is not None:
            for idx in range(1, self.sn_service_combo.count()):
                service_name = self.sn_service_combo.itemText(idx)
                if service_name == selected_service:
                    self.sn_service_combo.setCurrentIndex(idx)
                    break
        self.increment_spinbox.setValue(self.parent.preferences.sn_increment)
        self.station_id_spinbox.setValue(self.parent.preferences.station_id)
        super().exec()

    def accept(self):
        increment = self.increment_spinbox.value()
        station_id = self.station_id_spinbox.value()

        if station_id >= increment:
            QMessageBox.critical(self, 'Invalid Station Number',
                                 'Station id (%d) must be smaller than '
                                 'the serial-number increment (%d).'
                                 % (station_id, increment), QMessageBox.Ok)
            return
        super().accept()
        prefs = self.parent.preferences
        if self.sn_service_combo.currentIndex() == 0:
            prefs.sn_service = None
        else:
            prefs.sn_service = self.sn_service_combo.currentText()
        prefs.sn_increment = increment
        prefs.station_id = station_id
        prefs.save()
        self.parent.prefs_changed()

    def sn_service_changed(self):
        enable = (self.sn_service_combo.currentIndex() == 0)
        self.increment_spinbox.setEnabled(enable)
        self.station_id_spinbox.setEnabled(enable)

class UI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(window)

        self.params = {}

        ct_params = sensor_params.CT(Ui_Param_CT(), self.param_group,
                                     'CT Parameters')
        self.params['AC'] = self.params['DC'] = self.params['RC'] = ct_params
        self.params['voltage'] = sensor_params.Volt(Ui_Param_Volt(),
                                                    self.param_group,
                                                    'Voltage Parameters')
        self.params['temp'] = sensor_params.Temp(Ui_Param_Temp(),
                                                 self.param_group,
                                                 'Temperature Parameters')
        self.params['NTC'] = sensor_params.NTC(Ui_Param_NTC(), self.param_group,
                                               'NTC Thermistor Parameters')
        self.params['pulse'] = sensor_params.Pulse(Ui_Param_Pulse(),
                                                   self.param_group,
                                                   'Pulse Parameters')

        self.current_params = self.params['AC']
        self.current_params.activate()

        appicon = pkg_resources \
                  .resource_filename(__name__,
                                     'resources/icons/ctid-logo.png')
        window.setWindowIcon(QtGui.QIcon(appicon))
        self.auto_serial_checkbox.setChecked(True)
        self.serial_spinbox.setEnabled(False)
        self.console = terminal.Terminal(self.plainTextEdit)
        self.add_mfgs()
        self.busy = False
        self.cmd = None
        self.sn_service = None
        self.mfg_id = None
        self.model = None

        self.console.write('Welcome to the CTid Programmer!\n\n'
                           'You can use this tool to program '
                           'the microcontroller of a CTid board (PCB).\n\n'
                           'Please start by filling out the form on the left. '
                           'Then attach the programming cable to the '
                           'CTid board, and click "Program" to write the '
                           'information to the microcontroller.\n')
        self.welcome_msg = True	# we're displaying welcome message

        if not os.path.isdir(PATH_STATE_DIR):
            os.mkdir(PATH_STATE_DIR)
        self.preferences = preferences.Manager(PATH_STATE_DIR)
        self.sn = None
        self.template_manager = template.Manager(PATH_STATE_DIR)

        for st in ctid.SENSOR_TYPE_NAME:
            name = SENSOR_LONG_NAME[st] if st in SENSOR_LONG_NAME else st
            self.sensor_type_combo.addItem(name)

        self.sensor_type_combo.currentIndexChanged.connect(
            self.sensor_type_changed)
        self.mfg_combo.currentIndexChanged.connect(self.product_changed)
        self.model_lineEdit.editingFinished.connect(self.product_changed)
        self.auto_serial_checkbox.stateChanged.connect(self.auto_serial_changed)
        self.program_btn.clicked.connect(self.program_or_cancel)
        self.read_btn.clicked.connect(self.read)
        self.reprogram_after_cal_btn.clicked.connect(self.reprogram_after_cal)
        self.load_template_btn.clicked.connect(self.template_load)
        self.save_template_btn.clicked.connect(self.template_save)

        self.template_list_dialog = Template_List_Dialog(self)

        self.preferences_editor = Preferences_Editor(self)
        self.actionPreferences.triggered.connect(self.preferences_editor.exec)

        self.prefs_changed()

    def log(self, msg):
        if self.welcome_msg:
            self.plainTextEdit.clear()
            self.welcome_msg = False
        self.console.write(msg + '\n')

    def template_activate(self, template):
        '''Load values from template, except never load the serial-number.'''
        try:
            if 'model' in template:
                self.model_lineEdit.setText(template['model'])

            if 'mfg' in template:
                for idx in range(self.mfg_combo.count()):
                    if self.mfg_combo.itemData(idx) == template['mfg']:
                        # this may trigger call to product_changed() so
                        # model_lineEdit() must have been updated already...
                        self.mfg_combo.setCurrentIndex(idx)

            self.product_changed()

            self.sensor_type_combo.setCurrentIndex(0)
            for idx, code in enumerate(ctid.SENSOR_TYPE_NAME):
                if code == template['sensor_type']:
                    self.sensor_type_combo.setCurrentIndex(idx)
                    break

            self.r_source_spinbox.setValue(template['r_source'])
            self.r_load_spinbox.setValue(template['r_load'])

            if self.current_params is not None:
                self.current_params.load(template)
        except KeyError as key:
            QMessageBox.warning(self, 'Warning',
                                'Template is missing parameter %s.'
                                % (key), QMessageBox.Ok)

    def template_load(self):
        self.template_list_dialog.operation = 'load'
        self.template_list_dialog.template_name_frame.hide()
        self.template_list_dialog.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Open|QtGui.QDialogButtonBox.Cancel)
        self.template_list_dialog.exec()

    def template_save(self):
        self.template_list_dialog.operation = 'save'
        self.template_list_dialog.template_name_frame.show()
        self.template_list_dialog.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Save|QtGui.QDialogButtonBox.Cancel)
        self.template_list_dialog.exec()

    def get_mfg_id(self):
        mfg_idx = self.mfg_combo.currentIndex()
        if mfg_idx == 0:
            return None
        return self.mfg_combo.itemData(mfg_idx)

    def get_model(self):
        model = self.model_lineEdit.text().strip().lstrip()
        if not model:
            return None
        return model

    def update_sn(self):
        if not self.auto_serial_checkbox.isChecked():
            return

        if self.get_mfg_id() is None or self.get_model() is None:
            return

        next_sn = None
        try:
            next_sn = self.sn.get()
            if next_sn is None:
                QMessageBox.warning(self, 'Serial Number Unavailable',
                                    'Serial number service failed to return '
                                    'a serial number.  Reverting to '
                                    'manual serial numbers.',
                                    QMessageBox.Ok)
        except sn.SpaceExhausted:
            QMessageBox.warning(self, 'Serial Number Space Exhausted',
                                'All available serial-numbers have been used '
                                'for \"%s %s\".  Please use a different '
                                'manufacturer and/or model name.' \
                                % (ctid.mfg_short_name(self.mfg_id),
                                   self.model), QMessageBox.Ok)

        if next_sn is None:
            self.auto_serial_checkbox.setChecked(False)
            self.serial_spinbox.setEnabled(True)
            self.serial_spinbox.setValue(0)
            return

        self.serial_spinbox.setValue(next_sn)

    def sensor_type_changed(self):
        st = ctid.SENSOR_TYPE_NAME[self.sensor_type_combo.currentIndex()]
        new_params = self.params[st] if st in self.params else None

        if new_params == self.current_params:
            return	# no change

        if self.current_params is not None:
            self.current_params.deactivate()
        self.current_params = new_params

        if self.current_params is not None:
            self.current_params.activate()

    def product_changed(self):
        mfg_id = self.get_mfg_id()
        model = self.get_model()

        log.debug('product_changed: mfg_id=%s model=%s', mfg_id, model)

        if mfg_id is None or model is None:
            return

        if self.mfg_id == mfg_id and self.model == model:
            return	# no change
        self.mfg_id = mfg_id
        self.model = model

        if self.sn.set_product(mfg_id, model):
            self.update_sn()
        else:
            self.auto_serial_checkbox.setChecked(False)
            self.serial_spinbox.setValue(0)

    def auto_serial_changed(self):
        auto_serial = self.auto_serial_checkbox.isChecked()
        if auto_serial:
            latest_sn = self.serial_spinbox.value()
            self.sn.activate(latest_sn)
            self.update_sn()
        else:
            self.sn.deactivate()
        self.serial_spinbox.setEnabled(not auto_serial)

    def add_mfgs(self):
        '''Add companies per their table/manufacturer number as stated by CTid
        Spec Sheet.

        '''
        for mfg_id, name in ctid.MFG_ID.items():
            self.mfg_combo.addItem(name, mfg_id)

    def set_input_enabled(self, enabled):
        self.chip_combo.setEnabled(enabled)
        self.mfg_combo.setEnabled(enabled)
        self.sensor_type_combo.setEnabled(enabled)
        self.model_lineEdit.setEnabled(enabled)
        self.auto_serial_checkbox.setEnabled(enabled)
        self.r_source_spinbox.setEnabled(enabled)
        self.r_load_spinbox.setEnabled(enabled)

        serial_enabled = enabled and not self.auto_serial_checkbox.isChecked()
        self.serial_spinbox.setEnabled(serial_enabled)

        if self.current_params is not None:
            self.current_params.set_input_enabled(enabled)

        self.load_template_btn.setEnabled(enabled)
        self.save_template_btn.setEnabled(enabled)
        self.read_btn.setEnabled(enabled)
        self.reprogram_after_cal_btn.setEnabled(enabled)

    def cmd_start(self, argv, pattern_list, logfile=None):
        self.cmd = Command_Processor(argv, pattern_list, logfile=logfile)

    def cmd_done(self):
        if self.cmd.error is not None:
            self.log('Command failed: %s' % self.cmd.error)

    def get_template(self):
        '''Get form-data as a dictionary.  No validation is performed beyond
        the constraints imposed by the user-interface controls.

        '''
        template = {}

        mfg_id = self.get_mfg_id()
        if mfg_id is not None:
            template['mfg'] = mfg_id

        model = self.get_model()
        if model is not None:
            template['model'] = model

        template['sn'] = self.serial_spinbox.value()
        st_idx = self.sensor_type_combo.currentIndex()
        template['sensor_type'] = ctid.SENSOR_TYPE_NAME[st_idx]
        template['r_source'] = self.r_source_spinbox.value()
        template['r_load'] = self.r_load_spinbox.value()

        if self.current_params is not None:
            self.current_params.save(template)
        return template

    def validate_form(self):
        '''Validate form data and return cleaned data as a dictionary.'''
        cleaned_data = self.get_template()

        if 'mfg' not in cleaned_data:
            QMessageBox.warning(self, 'Manufacturer Missing',
                                'Please select manufacturer.', QMessageBox.Ok)
            self.mfg_combo.setFocus()
            return None

        if 'model' not in cleaned_data:
            QMessageBox.warning(self, 'Model Name Missing',
                                'Please enter model name.', QMessageBox.Ok)
            self.model_lineEdit.setFocus()
            return None

        utf8_model = cleaned_data['model'].encode('utf-8')
        if len(utf8_model) > 8:
            QMessageBox.warning(self, 'Model Name Too Long',
                                'Model name is %d bytes long in '
                                'UTF-8 encoding.  '
                                'Please limit name to 8 bytes in length.'
                                % len(utf8_model), QMessageBox.Ok)
            self.model_lineEdit.setFocus()
            return None
        return cleaned_data

    def show_cmd_error(self, cmd, title, msg):
        if cmd.exit_status is not None:
            msg += '  Exit status %d.' % cmd.exit_status
        QMessageBox.warning(self, title, msg, QMessageBox.Ok)

    def create_hexfile(self, cleaned_data, params):
        st = cleaned_data['sensor_type']
        argv = [PATH_CTID_ENCODER,
                '-M', '%d' % cleaned_data['mfg'],
                '-S', st,
                '-m', cleaned_data['model'],
                '-n', '%d' % cleaned_data['sn'],
                '-l', '%d' % cleaned_data['r_load'],
                '-r', '%d' % cleaned_data['r_source']]

        if params is not None:
            argv += params.encoder_argv(cleaned_data)

        output = tempfile.mkstemp(suffix='.hex', prefix='CTid-')
        argv += ['-o', output[1]]

        template_filename = CODE_TEMPLATE[st] if st in CODE_TEMPLATE \
                            else 'powered.hex'
        argv.append(os.path.join(PATH_CODE_DIR, template_filename))

        log.debug('create_hexfile: argv=%s', argv)

        self.cmd_start(argv, [], logfile=self.console)
        for _ in self.cmd:
            pass
        self.cmd_done()
        if self.cmd.exit_status != 0:
            self.show_cmd_error(self.cmd, 'Command Failed',
                                'Failed to create hex file.')
            os.close(output[0])
            os.remove(output[1])
            return None

        # now that we have created the actual hexfile, it's safe to close
        # the original (empty) file created by mkstemp():
        os.close(output[0])
        return output[1]

    def detect_chip_type(self):
        self.cmd_start([PATH_AVRDUDE, '-ctc2030', '-pt9', '-nq'],
                       [r'Device signature = 0x([0-9a-f]+)'])
        chip_id = None
        for _, match in self.cmd:
            chip_id = int(match.group(1), base=16)
        self.cmd_done()
        if chip_id is None:
            QMessageBox.warning(self, 'No Microcontroller Detected',
                                'No microcontroller detected.  '
                                'Please confirm programming cable is '
                                'properly attached.',
                                QMessageBox.Ok)
            return None
        if chip_id not in CHIP_ID_TO_NAME:
            QMessageBox.warning(self, 'Unknown Microcontroller',
                                'Unknown microcontroller chip type 0x%x.'
                                % chip_id, QMessageBox.Ok)
            return None
        chip = CHIP_ID_TO_NAME[chip_id]
        self.log('Detected %s chip.' % chip[1])
        return chip[0]

    def write_flash(self, chip_type, hexfile, cleaned_data):
        self.cmd_start([PATH_AVRDUDE, '-ctc2030', '-p%s' % chip_type,
                        '-Uflash:w:%s' % hexfile], [], logfile=self.console)
        for _ in self.cmd:
            pass	# consume output until program is done...
        self.cmd_done()
        if self.cmd.exit_status == 0:
            self.log('Success: CTid board has been programmed with '
                     'serial number %d.' % cleaned_data['sn'])
            self.sn.commit(cleaned_data['sn'], cleaned_data)
            self.update_sn()
        else:
            self.show_cmd_error(self.cmd, 'Programming Failed',
                                'Failed to write the microcontroller flash.')
            return

    def read_template_from_flash(self, chip_type):
        temp = tempfile.mkstemp(suffix='.bin', prefix='CTid-')
        self.cmd_start([PATH_AVRDUDE, '-ctc2030', '-p%s' % chip_type,
                        '-Uflash:r:%s:r' % temp[1]], [], logfile=self.console)
        for _ in self.cmd:
            pass	# consume output until program is done...
        self.cmd_done()

        if self.cmd.exit_status != 0:
            os.close(temp[0])
            os.remove(temp[1])
            self.show_cmd_error(self.cmd, 'Read Failed',
                                'Failed to read the microcontroller flash.')
            return None

        flash = open(temp[1], 'rb').read()
        os.close(temp[0])
        os.remove(temp[1])

        if len(flash) < 0x3e1:
            if not flash:
                QMessageBox.critical(self, 'Read Failed',
                                     'Microcontroller flash is empty.',
                                     QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Read Failed',
                                     'Read only %u bytes from '
                                     'microcontroller flash.'
                                     % len(flash), QMessageBox.Ok)
            return None
        self.log('Success: CTid board has been read.')

        CTid_table_addr = 0x3c0		# table goes in last 64 bytes
        length = flash[CTid_table_addr]
        table = flash[CTid_table_addr + 1:CTid_table_addr + 1 + length]
        table = ctid.Table(ctid.unstuff(table))
        return self.ctid_table_to_template(table)

    def reprogram_with_cal_params(self, chip_type):
        template = self.read_template_from_flash(chip_type)
        if template is None:
            return

        self.sn.set_product(template['mfg'], template['model'])

        cal_params = self.sn.get_cal_data(template['sn'])
        if cal_params is None:
            QMessageBox.critical(self, 'No Calibration Data Found',
                                 'No calibration data was found for '
                                 'product %s with serial number %s.' %
                                 (self.sn.product, template['sn']),
                                 QMessageBox.Ok)
            return

        msg = ''
        for key, value in cal_params.items():
            msg += '\t%16s: %s\n' % (key, value)

        self.console.write('\n\nFound calibration parameters:\n%s\n' % msg)

        # merge the calibrated parameters with existing template:
        for name, value in cal_params.items():
            template[name] = value

        hexfile = self.create_hexfile(template,
                                      self.params[template['sensor_type']])
        if hexfile is None:
            self.mark_idle()
            return
        self.write_flash(chip_type, hexfile, template)
        os.remove(hexfile)
        self.mark_idle()

    def read_flash(self, chip_type):
        template = self.read_template_from_flash(chip_type)
        if template is None:
            return
        self.template_activate(template)
        self.auto_serial_checkbox.setChecked(False)
        self.serial_spinbox.setValue(template['sn'])

    def ctid_table_to_template(self, table):
        sensor_type = ctid.SENSOR_TYPE_NAME[table.sensor_type]
        template = {}
        template['mfg'] = table.mfg_id
        template['model'] = table.model
        template['sn'] = table.serial_number
        template['sensor_type'] = sensor_type
        template['r_source'] = table.r_source
        template['r_load'] = table.r_load
        self.params[sensor_type].table_to_template(table, template)
        return template

    def mark_busy(self):
        self.plainTextEdit.clear()
        self.busy = True
        self.set_input_enabled(False)
        self.program_btn.setText('Cancel')

    def mark_idle(self):
        self.busy = False
        self.program_btn.setText('Program')
        self.set_input_enabled(True)

    def chip_type(self):
        if self.chip_combo.currentIndex() == 0:
            # auto-detect chip
            chip_type = self.detect_chip_type()
        elif self.chip_combo.currentIndex() == 1:
            chip_type = 't9'
        else:
            chip_type = 't10'
        return chip_type

    def program_or_cancel(self):
        '''Program the microcontroller with the info specified in the form.
        This consists of two steps: (1) creating a hex file with the
        info encoded and (2) writing the file to the microcontroller.

        '''
        if self.busy:
            if self.cmd is not None:
                self.cmd.stop()	# cancel the running command
                self.cmd_done()
            self.mark_idle()
            return

        cleaned_data = self.validate_form()
        if cleaned_data is None:
            return

        self.mark_busy()

        hexfile = self.create_hexfile(cleaned_data, self.current_params)
        if hexfile is None:
            self.mark_idle()
            return

        chip_type = self.chip_type()
        if chip_type is not None:
            self.write_flash(chip_type, hexfile, cleaned_data)

        os.remove(hexfile)
        self.mark_idle()

    def read(self):
        '''Reads CTid parameters from the flash.'''
        self.mark_busy()

        chip_type = self.chip_type()
        if chip_type is not None:
            self.read_flash(chip_type)

        self.mark_idle()

    def reprogram_after_cal(self):
        '''Reads CTid parameters from the flash, lookup calibration parameters
        for the read serial-number and, if that exists, reprogram with
        those parameters.

        '''
        self.mark_busy()

        chip_type = self.chip_type()
        if chip_type is not None:
            self.reprogram_with_cal_params(chip_type)

        self.mark_idle()

    def prefs_changed(self):
        prefs = self.preferences

        if self.sn is None or self.sn_service != prefs.sn_service:
            self.sn_service = prefs.sn_service
            if prefs.sn_service == 'eGauge':
                self.sn = sn_egauge.Manager(self, PATH_STATE_DIR)
            else:
                if prefs.sn_service is not None:
                    QMessageBox.critical(self, 'Unknown Serial Number Service',
                                         'Serial number service %s is '
                                         'unknown.  Reverting to locally '
                                         'managed serial numbers.' \
                                         % prefs.sn_service)
                    self.sn_service = None
                self.sn = sn_local.Manager(self, PATH_STATE_DIR)
            if self.mfg_id is not None and self.model is not None:
                self.sn.set_product(self.mfg_id, self.model)
            self.reprogram_after_cal_btn.setVisible(
                self.sn.has_calibration_data())
        self.sn.set_preferences(prefs)
        self.update_sn()

parser = argparse.ArgumentParser(description='CTid GUI programmer.')
parser.add_argument('-F', '--full-screen', action='store_true',
                    help='Start application in full-screen mode.')
parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG,
                    dest='log_level', help='Show debug output.')
args = parser.parse_args()

log_level = logging.ERROR if args.log_level is None else args.log_level
logging.basicConfig()
log = logging.getLogger()	# get the root logger
log.setLevel(log_level)		# sets default logging for all child loggers

app = QApplication(sys.argv)
window = QMainWindow()
ui = UI()

if args.full_screen:
    window.showMaximized()
else:
    window.show()
sys.exit(app.exec_())

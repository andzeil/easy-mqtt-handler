"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  qt/tabs/PayloadTabWidget.py
*
*  Defines the Payload Editor Tab
*
*  Copyright (C) 2023 A. Zeil
"""
import gettext
import os

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QPushButton, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QSizePolicy, QTableWidgetItem, QFileDialog

from easy_mqtt_handler.util.MQTTPayloads import MQTTPayloads
from easy_mqtt_handler.util.Tools import Utils

# Set the local directory
localedir = Utils.resource_path("./locale")

# Set up your magic function
translate = gettext.translation("PayloadTabWidget", localedir, fallback=True)
_ = translate.gettext


class PayloadTabWidget(QWidget):

    settings_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        # create the table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([_('Payload Command'), _('Payload Argument'),
                                              _('Command to Run'), "", _('Command line arguments')])

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        # create the buttons
        self.save_button = QPushButton(_('Add Payload'))
        self.save_button.clicked.connect(self.add_payload)
        self.cancel_button = QPushButton(_('Remove Payload'))
        self.cancel_button.clicked.connect(self.remove_payload)

        # create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)

    def setting_changed_event(self, text):
        self.settings_changed.emit(True)
        self.set_new_payload_data()

    def add_data(self, payload_command, payload_argument, command_to_run, command_line_arguments):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)

        self.table.setItem(row_count, 0, QTableWidgetItem(payload_command))
        self.table.setItem(row_count, 1, QTableWidgetItem(payload_argument))
        self.table.setItem(row_count, 2, QTableWidgetItem(command_to_run))

        button = QPushButton("...")
        button.setFixedWidth(40)
        button.setProperty("row", row_count)
        self.table.setCellWidget(row_count, 3, button)
        button.clicked.connect(lambda: self.browse_executable(button))

        self.table.setItem(row_count, 4, QTableWidgetItem(command_line_arguments))

    def browse_executable(self, cur_button):

        # set some options for the file open dialog if we are on windows
        if os.name == "nt":
            start_dir = "C:\\"
            file_filter = "*.*"
        # or on linux and macOS
        else:
            start_dir = "/"
            file_filter = "*"

        filedialog = QFileDialog()
        filedialog.setWindowTitle(_('Select an executable file'))
        filedialog.setDirectory(start_dir)
        filedialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        filedialog.setNameFilter(file_filter)
        filedialog.setViewMode(QFileDialog.ViewMode.List)

        if filedialog.exec_() and len(filedialog.selectedFiles()) == 1:
            selected_file = filedialog.selectedFiles()[0]
            self.table.item(cur_button.property("row"), 2).setText(selected_file)
            self.table.viewport().update()

    def add_payload(self):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)

        self.table.setItem(row_count, 0, QTableWidgetItem(""))
        self.table.setItem(row_count, 1, QTableWidgetItem(""))
        self.table.setItem(row_count, 2, QTableWidgetItem(""))

        button = QPushButton("...")
        button.setFixedWidth(40)
        button.setProperty("row", row_count)
        self.table.setCellWidget(row_count, 3, button)
        button.clicked.connect(lambda: self.browse_executable(button))

        self.setting_changed_event(True)

    def set_new_payload_data(self):
        # ensure payload data is empty
        new_payload_data = []
        # payload_data.clear()

        # for each line of the table append one item to the payload config
        for row in range(self.table.rowCount()):
            payload_command = "" if self.table.item(row, 0) is None else self.table.item(row, 0).text()
            payload_argument = "" if self.table.item(row, 1) is None else self.table.item(row, 1).text()
            command_to_run = "" if self.table.item(row, 2) is None else self.table.item(row, 2).text()
            command_line_arguments = "" if self.table.item(row, 4) is None else self.table.item(row, 4).text()
            new_payload_data.append({
                'payload_command': payload_command,
                'payload_argument': payload_argument,
                'command_to_run': command_to_run,
                'command_line_arguments': command_line_arguments
            })

        MQTTPayloads.get_instance().payload_data = new_payload_data

    def remove_payload(self):
        selected_row = self.table.currentRow()
        self.table.removeRow(selected_row)
        self.setting_changed_event(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        # unbind dataChanged event until we've loaded the new payload data
        self.table.model().dataChanged.disconnect()

        payload_settings = MQTTPayloads.get_instance().payload_data

        # clear the table to get a fresh copy of the payload config
        self.table.clearContents()
        self.table.setRowCount(0)

        # fill table with current payload config
        for item in payload_settings:
            self.add_data(str(item['payload_command']),
                          str(item['payload_argument']),
                          str(item['command_to_run']),
                          str(item['command_line_arguments']))

        # now that we've loaded data: enable listening to dataChanged event and send a signal on changes
        self.table.model().dataChanged.connect(self.setting_changed_event)

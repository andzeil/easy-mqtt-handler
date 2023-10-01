"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  qt/tabs/LogTabWidget.py
*
*  Defines the Logging tab
*
*  Copyright (C) 2023 A. Zeil
"""
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class LogTabWidget(QWidget):
    def __init__(self):
        super().__init__()

        # create the multi-line text box
        self.text_box = QTextEdit(self)
        self.text_box.setReadOnly(True)

        # make it always fill the QWidget
        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        self.setLayout(layout)

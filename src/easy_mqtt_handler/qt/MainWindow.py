"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  qt/MainWindow.py
*
*  Main window of the program based on QMainWindow (QT5)
*
*  Copyright (C) 2023 A. Zeil
"""
import gettext
import sys

from PyQt5.QtCore import QSize, QThread
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QTabWidget, QSystemTrayIcon, QMenu, QStatusBar, QLabel, \
    QMessageBox

from easy_mqtt_handler.qt.AboutDialog import AboutDialog
from easy_mqtt_handler.qt.tabs.ConnectionTabWidget import ConnectionTabWidget
from easy_mqtt_handler.qt.tabs.LogTabWidget import LogTabWidget
from easy_mqtt_handler.qt.tabs.PayloadTabWidget import PayloadTabWidget

from easy_mqtt_handler.util.Icons import *
from easy_mqtt_handler.util.MQTTPayloads import MQTTPayloads
from easy_mqtt_handler.util.MQTTSettings import MQTTSettings
from easy_mqtt_handler.util.MQTTWorkerThread import MQTTWorkerThread
from easy_mqtt_handler.util.Tools import Utils

# Set the local directory
localedir = Utils.resource_path("./locale")

# Set up your magic function
translate = gettext.translation("MainWindow", localedir, fallback=True)
_ = translate.gettext

# consts go here
PROG_NAME = _("Easy MQTT Handler")

# get locations of config files
config_path = Utils.get_config_path()
payload_file = config_path + "default-payloads.json"
settings_file = config_path + "default-settings.json"


class MainWindow(QMainWindow):
    tab_widget: QTabWidget
    settings: MQTTSettings
    payloads: MQTTPayloads
    unsaved_changes = False

    """
    Main Window init()
    """

    def __init__(self, app, mqtt_config_file, payload_config_file):
        super().__init__()

        self.worker_thread: QThread

        self.setWindowTitle(PROG_NAME)
        app.setQuitOnLastWindowClosed(False)

        # load current configs
        self.settings = MQTTSettings(mqtt_config_file if mqtt_config_file != "" else settings_file)
        self.payloads = MQTTPayloads(payload_config_file if payload_config_file != "" else payload_file)

        # load the dialog icon
        self.setWindowIcon(Icons.load_icon(APP_ICON))

        # create toolbar
        toolbar = QToolBar(self)
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        # create tab container widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # as long as we init. the tabs, block signals
        self.tab_widget.blockSignals(True)

        # create the tabs
        self.log_tab = LogTabWidget()
        self.connection_tab = ConnectionTabWidget()
        self.payload_editor = PayloadTabWidget()

        # add them to the tab widget
        self.tab_widget.addTab(self.connection_tab, _("Connection"))
        self.tab_widget.addTab(self.payload_editor, _("Payload Handlers"))
        self.tab_widget.addTab(self.log_tab, _("Logs"))

        # wire change handlers
        self.connection_tab.settings_changed.connect(self.on_connection_settings_changed)
        self.payload_editor.settings_changed.connect(self.on_payloads_changed)

        # now that init is done receive signals again
        self.tab_widget.blockSignals(False)

        # create a worker thread and connect the signal to update the main form
        self.worker_thread = MQTTWorkerThread()
        self.worker_thread.add_log_line.connect(self.add_log_line)
        self.worker_thread.track_status.connect(self.track_status)

        # start the worker thread
        self.worker_thread.start()

        # create an About dialog ... we might need it later
        self.about_dialog = AboutDialog(app)

        # add actions to toolbar
        self.save_action = QAction(Icons.load_icon(TOOLBAR_SAVE), _("Save"), self)
        self.save_action.triggered.connect(self.save_settings)
        self.save_action.setVisible(False)
        toolbar.addAction(self.save_action)

        self.action_seperator = toolbar.addSeparator()
        self.action_seperator.setVisible(False)

        self.connect_action = QAction(Icons.load_icon(TOOLBAR_CONNECT), _("Connect"), self)
        self.connect_action.triggered.connect(self.on_connect_action)
        toolbar.addAction(self.connect_action)

        self.disconnect_action = QAction(Icons.load_icon(TOOLBAR_DISCONNECT), _("Disconnect"), self)
        self.disconnect_action.triggered.connect(self.worker_thread.mqtt_disconnect)
        toolbar.addAction(self.disconnect_action)

        self.reconnect_action = QAction(Icons.load_icon(TOOLBAR_RECONNECT), _("Reconnect"), self)
        self.reconnect_action.triggered.connect(self.worker_thread.mqtt_reconnect)
        toolbar.addAction(self.reconnect_action)

        toolbar.addSeparator()

        self.about_action = QAction(Icons.load_icon(TOOLBAR_ABOUT), _("About"), self)
        self.about_action.triggered.connect(self.about_dialog.show)
        toolbar.addAction(self.about_action)

        self.quit_action = QAction(Icons.load_icon(TOOLBAR_QUIT), _("Quit"), self)
        self.quit_action.triggered.connect(self.on_close)
        toolbar.addAction(self.quit_action)

        # let's create a statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_icon = QLabel()
        self.status_icon.setPixmap(Icons.load_icon(STATUSBAR_DISCONNECTED).pixmap(32))
        self.status_icon.setToolTip(_("Disconnected"))
        self.statusbar.addPermanentWidget(self.status_icon)

        # let's set up a tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(Icons.load_icon(APP_ICON))
        self.tray_icon.setToolTip(PROG_NAME)
        self.tray_icon.setVisible(True)

        # add a tiny context menu to the tray icon
        tray_menu = QMenu(self)

        # assign some actions to the context menu
        action_open = tray_menu.addAction(_("Open"))
        action_open.triggered.connect(self.on_tray_open)

        action_close = tray_menu.addAction(_("Close"))
        action_close.triggered.connect(self.on_close)

        # add the context menu to the tray icon
        self.tray_icon.setContextMenu(tray_menu)

        # wire event handler
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # resize and reposition main window
        self.width = app.primaryScreen().size().width() // 4
        self.height = app.primaryScreen().size().height() // 4
        pos_x = app.primaryScreen().size().width() // 2
        pos_y = app.primaryScreen().size().height() // 2
        self.setGeometry(pos_x - (self.width // 2), pos_y - (self.height // 2), self.width, self.height)

    """
    Event Handlers
    """
    def on_close(self):
        if self.unsaved_changes:
            confirm_quit = QMessageBox(self)
            confirm_quit.setWindowTitle(_("Unsaved changes detected."))
            confirm_quit.setText(_("You haven't saved your changes, yet. Do you still want to quit?"))
            confirm_quit.setStandardButtons(QMessageBox.Ok | QMessageBox.Save | QMessageBox.Cancel)
            selected_button = confirm_quit.exec()
            if selected_button == QMessageBox.Ok:
                sys.exit(0)
            elif selected_button == QMessageBox.Save:
                self.save_settings()
                confirm_final_quit = QMessageBox(self)
                confirm_final_quit.setWindowTitle(_("Settings saved."))
                confirm_final_quit.setText(_("Do you want to quit the application now?"))
                confirm_final_quit.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                selected_button = confirm_final_quit.exec()
                if selected_button == QMessageBox.Yes:
                    sys.exit(0)
                elif selected_button == QMessageBox.No:
                    return

            elif selected_button == QMessageBox.Cancel:
                return
        else:
            sys.exit(0)

    # will be called when the tray icon is interacted with
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def on_tray_open(self):
        self.show()
        self.activateWindow()
        self.raise_()

    def on_connection_settings_changed(self, changed):
        self.setWindowTitle("*" + PROG_NAME)
        self.tab_widget.setTabText(0, "*" + _("Connection"))
        self.unsaved_changes = True
        self.save_action.setVisible(True)
        self.action_seperator.setVisible(True)

    def on_payloads_changed(self, changed):
        self.setWindowTitle("*" + PROG_NAME)
        self.tab_widget.setTabText(1, "*" + _("Payload Handlers"))
        self.unsaved_changes = True
        self.save_action.setVisible(True)
        self.action_seperator.setVisible(True)

    def on_connect_action(self):
        if self.worker_thread.mqtt_connect():
            self.connect_action.setEnabled(False)
            self.disconnect_action.setVisible(True)
            self.add_log_line(_("Connecting to Broker, please wait ..."))

    def add_log_line(self, text):
        logline = f"[{Utils.get_timestamp()}] {text}"
        self.statusbar.showMessage(logline)
        self.log_tab.text_box.append(logline)
        self.statusbar.setToolTip(text)

    def track_status(self, code):
        match code:
            case 100:
                self.status_icon.setPixmap(Icons.load_icon(STATUSBAR_DISCONNECTED).pixmap(32))
                self.status_icon.setToolTip(_("Disconnected"))

            case 102 | 103 | 104:
                self.disconnect_action.setVisible(False)
                self.reconnect_action.setVisible(False)
                self.tab_widget.setCurrentIndex(2)

            case 101:
                self.connect_action.setVisible(False)
                self.status_icon.setPixmap(Icons.load_icon(STATUSBAR_CONNECTED).pixmap(32))
                self.status_icon.setToolTip(_("Connected"))
                self.connect_action.setEnabled(True)

            case 105:
                self.connect_action.setEnabled(True)

            case 200:
                self.tab_widget.setCurrentIndex(0)

            case 300:
                self.disconnect_action.setVisible(True)
                self.reconnect_action.setVisible(True)
                self.status_icon.setPixmap(Icons.load_icon(STATUSBAR_CONNECTED).pixmap(32))
                self.status_icon.setToolTip(_("Connected"))

            case 301:
                self.connect_action.setVisible(True)
                self.disconnect_action.setVisible(False)
                self.reconnect_action.setVisible(False)
                self.status_icon.setPixmap(Icons.load_icon(STATUSBAR_DISCONNECTED).pixmap(32))
                self.status_icon.setToolTip(_("Disconnected"))

            case 302:
                self.connect_action.setVisible(False)
                self.disconnect_action.setVisible(True)
                self.reconnect_action.setVisible(True)
                self.status_icon.setPixmap(Icons.load_icon(STATUSBAR_DISCONNECTED).pixmap(32))
                self.status_icon.setToolTip(_("Disconnected"))

            case _:
                self.add_log_line(_("Statuscode {0} not implemented!").format(code))

    def closeEvent(self, event):
        # don't allow to close the main window
        event.ignore()
        self.hide()

    """
    Helpers
    """

    def save_settings(self):
        if MQTTSettings.get_instance().save_settings():
            # remove mark from tab title
            self.tab_widget.setTabText(0, _("Connection"))

        if MQTTPayloads.get_instance().save_payload_data():
            # remove mark from tab title
            self.tab_widget.setTabText(1, _("Payload Handlers"))

        self.setWindowTitle(PROG_NAME)
        self.unsaved_changes = False
        self.save_action.setVisible(False)
        self.action_seperator.setVisible(False)

#! /usr/bin/python3
"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  __main__.py
*
*  Main class of the program
*
*  Copyright (C) 2023 A. Zeil
"""
import sys
import argparse

from PyQt5.QtWidgets import QApplication
from easy_mqtt_handler.qt.MainWindow import MainWindow
from easy_mqtt_handler.util.Tools import Utils


# entry point
if __name__ == "__main__":

    arguments = argparse.ArgumentParser(description="Easy MQTT Handler")
    arguments.add_argument("-mqtt-conf", "--mqtt-configuration-file", type=str, default="")
    arguments.add_argument("-payload-conf", "--payload-configuration-file", type=str, default="")
    args = arguments.parse_args()

    # create configuration folder, if it doesn't exist, yet
    firstStart = Utils.create_path_if_not_exists(Utils.get_config_path())

    # create the application
    app = QApplication(sys.argv)

    # create the main window
    main_window = MainWindow(app, args.mqtt_configuration_file, args.payload_configuration_file)

    # if this is our first run, show the main window
    if firstStart:
        main_window.show()

    # run the application
    sys.exit(app.exec_())

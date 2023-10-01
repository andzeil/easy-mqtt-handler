"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  Tools.py
*
*  This class contains a collection of various utility functions
*
*  Copyright (C) 2023 A. Zeil
"""
import datetime
import os
import sys

from pathlib import Path


class Utils:
    @staticmethod
    def get_config_path():
        # on windows, we want to store the configuration in %appdata%\easy-mqtt-handler, while
        # on *nix-based OSes we want to store the configuration in ~/.config/easy-mqtt-handler
        return os.path.expandvars("%appdata%\\easy-mqtt-handler\\") if os.name == "nt" else os.path.expanduser("~/.config/easy-mqtt-handler/")

    @staticmethod
    def create_path_if_not_exists(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            return True
        else:
            return False

    @staticmethod
    def get_timestamp():
        return datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S")

    @staticmethod
    def load_license_file(license_file):
        if os.path.exists(license_file):
            try:
                sf = open(license_file, 'r')
                return sf.read()
            # TODO: implement better exception handling
            except IOError:
                return "License File couldn't be loaded, please check our Git Repository: https://github.com/azeil/easy-mqtt-handler/"
        else:
            return "License File couldn't be loaded, please check our Git Repository: https://github.com/azeil/easy-mqtt-handler/"

    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', str(Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()))
        return os.path.join(base_path, relative_path)

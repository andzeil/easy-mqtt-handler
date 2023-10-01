"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  util/Icons.py
*
*  Class to handle program icons
*
*  Copyright (C) 2023 A. Zeil
"""
from PyQt5.QtGui import QIcon

from easy_mqtt_handler.util.Tools import Utils

# the default icons are all part of the "Humanity" Icon set (see license-humanity.txt)
APP_ICON = Utils.resource_path("assets/app-icon/app-icon.svg")

BUTTON_ADD = Utils.resource_path("assets/button/add.svg")
BUTTON_CLEAR = Utils.resource_path("assets/button/clear.svg")
BUTTON_COPY = Utils.resource_path("assets/button/copy.svg")
BUTTON_REMOVE = Utils.resource_path("assets/button/remove.svg")

TOOLBAR_ABOUT = Utils.resource_path("assets/toolbar/about.svg")
TOOLBAR_CONNECT = Utils.resource_path("assets/toolbar/connect.svg")
TOOLBAR_DISCONNECT = Utils.resource_path("assets/toolbar/disconnect.svg")
TOOLBAR_QUIT = Utils.resource_path("assets/toolbar/quit.svg")
TOOLBAR_RECONNECT = Utils.resource_path("assets/toolbar/reconnect.svg")
TOOLBAR_SAVE = Utils.resource_path("assets/toolbar/save.svg")

STATUSBAR_CONNECTED = Utils.resource_path("assets/statusbar/connected.svg")
STATUSBAR_DISCONNECTED = Utils.resource_path("assets/statusbar/disconnected.svg")


class Icons(object):
    @staticmethod
    def load_icon(icon_filename):
        try:
            return QIcon(icon_filename)
        # TODO: implement better exception handling
        except:
            return None

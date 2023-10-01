"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  util/MQTTSettings.py
*
*  Class to handle MQTT connection settings
*
*  Copyright (C) 2023 A. Zeil
"""
import json
import os


class MQTTSettings(object):

    @property
    def hostname(self):
        return self.get_property('hostname')

    @hostname.setter
    def hostname(self, value):
        self.hostname = value

    @property
    def port(self):
        return self.get_property('port')

    @port.setter
    def port(self, value):
        self.port = value

    @property
    def username(self):
        return self.get_property('username')

    @username.setter
    def username(self, value):
        self.username = value

    @property
    def password(self):
        return self.get_property('password')

    @password.setter
    def password(self, value):
        self.password = value

    @property
    def topic(self):
        return self.get_property('topic')

    @topic.setter
    def topic(self, value):
        self.topic = value

    @property
    def enable_ssl(self):
        if self.get_property('enable_ssl') is None:
            return False
        else:
            return self.get_property('enable_ssl')

    @enable_ssl.setter
    def enable_ssl(self, value):
        self.enable_ssl = value

    @property
    def server_certificate_file(self):
        return self.get_property('server_certificate_file')

    @server_certificate_file.setter
    def server_certificate_file(self, value):
        self.server_certificate_file = value

    @property
    def enable_client_ssl_auth(self):
        if self.get_property('enable_client_ssl_auth') is None:
            return False
        else:
            return self.get_property('enable_client_ssl_auth')

    @enable_client_ssl_auth.setter
    def enable_client_ssl_auth(self, value):
        self.enable_client_ssl_auth = value

    @property
    def client_certificate_file(self):
        return self.get_property('client_certificate_file')

    @client_certificate_file.setter
    def client_certificate_file(self, value):
        self.client_certificate_file = value

    @property
    def client_key_file(self):
        return self.get_property('client_key_file')

    @client_key_file.setter
    def client_key_file(self, value):
        self.client_key_file = value

    @property
    def allow_insecure_ssl(self):
        if self.get_property('allow_insecure_ssl') is None:
            return False
        else:
            return self.get_property('allow_insecure_ssl')

    @allow_insecure_ssl.setter
    def allow_insecure_ssl(self, value):
        self.allow_insecure_ssl = value

    _instance = None
    _filename = ""
    _settings = {}

    @staticmethod
    def get_instance():
        if MQTTSettings._instance is None:
            MQTTSettings()
        return MQTTSettings._instance

    def __init__(self, filename):
        if MQTTSettings._instance is not None:
            raise Exception("This is a Singleton Class. Only once instance allowed!")
        else:
            MQTTSettings._instance = self
            self._filename = filename
            self._settings = self.load_settings()

    def get_property(self, property_name):
        try:
            if property_name not in self._settings.keys():
                return None
            return self._settings[property_name]
        except AttributeError:
            return None

    def load_settings(self):
        self._settings.clear()

        if os.path.exists(self._filename):
            try:
                sf = open(self._filename, 'r')
                return json.load(sf)
            # TODO: implement better exception handling
            except IOError:
                # self.add_log_line("Settings File couldn't be loaded.")
                return ""
        else:
            # self.add_log_line("Settings File doesn't exist, yet.")
            return ""

    def refresh_settings(self, new_settings):
        self._settings = new_settings

    def save_settings(self):
        try:
            with open(self._filename, 'w') as sf:
                json.dump(self._settings, sf)
                sf.close()

                return True
        # TODO: implement better exception handling
        except:
            return False

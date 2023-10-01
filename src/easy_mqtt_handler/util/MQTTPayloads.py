"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  util/MQTTPayloads.py
*
*  Class to handle MQTT payloads
*
*  Copyright (C) 2023 A. Zeil
"""
import json
import os


class MQTTPayloads(object):
    @property
    def payload_data(self):
        return self._payload_data

    @payload_data.setter
    def payload_data(self, value):
        self._payload_data = value

    _instance = None
    _payload_file = ""

    _payload_data = {}

    @staticmethod
    def get_instance():
        if MQTTPayloads._instance is None:
            MQTTPayloads()
        return MQTTPayloads._instance

    def __init__(self, filename):
        if MQTTPayloads._instance is not None:
            raise Exception("This is a Singleton Class. Only once instance allowed!")
        else:
            MQTTPayloads._instance = self
            self._payload_file = filename
            self._payload_data = self.load_payload_data()

    def load_payload_data(self):
        self._payload_data.clear()

        if os.path.exists(self._payload_file):
            try:
                pf = open(self._payload_file, 'r')
                return json.load(pf)
            # TODO: implement better exception handling
            except IOError:
                # self.add_log_line("Payload File couldn't be loaded.")
                return ""
        else:
            # self.add_log_line("Payload File doesn't exist, yet.")
            return ""

    def save_payload_data(self):
        # create a JSON object from the data and save it to the payload config file
        try:
            with open(self._payload_file, 'w') as pf:
                json.dump(self._payload_data, pf)
                pf.close()

                return True
        # TODO: implement better exception handling
        except:
            return False

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
import socket
import sys

from cryptography.hazmat.primitives import serialization
from OpenSSL import SSL
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
                return "License File couldn't be loaded, please check our Git Repository: " \
                       "https://github.com/andzeil/easy-mqtt-handler/"
        else:
            return "License File couldn't be loaded, please check our Git Repository: " \
                   "https://github.com/andzeil/easy-mqtt-handler/"

    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', str(Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()))
        return os.path.join(base_path, relative_path)

    # this function tries to establish a connection and initiate an SSL handshake to fetch the certificate chain from a
    # server. it returns False, should it not be able to do so for whatever reason
    @classmethod
    def get_certificate_chain(cls, host, port):
        try:
            ssl_context = SSL.Context(method=SSL.SSLv23_METHOD)
            ssl_connection = SSL.Connection(ssl_context,
                                            socket=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM))
            # ssl_connection.settimeout(1)
            ssl_connection.setblocking(1)
            ssl_connection.connect((host, int(port)))
            ssl_connection.do_handshake()
            cert_chain = ssl_connection.get_peer_cert_chain()
            ssl_connection.close()

            pem_file_bytes = bytearray()
            for cert in cert_chain:
                pem_file_bytes = pem_file_bytes + cert.to_cryptography().public_bytes(serialization.Encoding.PEM)

            tmp_pem_file = f"{cls.get_config_path()}tmp.pem"

            with open(tmp_pem_file, 'wb') as pf:
                pf.write(pem_file_bytes)
                pf.close()

                return tmp_pem_file
        except:
            return False

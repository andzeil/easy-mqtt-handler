"""
SPDX-License-Identifier: GPL-3.0-or-later
*
*  util/MQTTWorkerThread.py
*
*  Class defines the WorkerThread to handle the MQTT connection
*
*  Copyright (C) 2023 A. Zeil
"""
import gettext
import json
import os
from ssl import SSLError, SSLZeroReturnError

from PyQt5.QtCore import QThread, pyqtSignal
import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl

from easy_mqtt_handler.util.MQTTPayloads import MQTTPayloads
from easy_mqtt_handler.util.MQTTSettings import MQTTSettings
from easy_mqtt_handler.util.Tools import Utils

# Set the local directory
localedir = Utils.resource_path("./locale")

# Set up your magic function
translate = gettext.translation('MQTTWorkerThread', localedir, fallback=True)
_ = translate.gettext


def extract_payload(payload):
    try:
        return json.loads(payload.decode())
    except Exception:
        return payload.decode()


def find_command_to_run(command, arg):
    payload_data = MQTTPayloads.get_instance().payload_data

    for item in payload_data:
        if item['payload_command'] == command and item['payload_argument'] == arg:
            return item['command_to_run']
    return None


def find_command_line_arguments(command, arg):
    payload_data = MQTTPayloads.get_instance().payload_data

    for item in payload_data:
        if item['payload_command'] == command and item['payload_argument'] == arg:
            return item['command_line_arguments']
    return None


class MQTTWorkerThread(QThread):
    # create a signal for adding a log line -> we need this cause we are running in a separate thread
    add_log_line = pyqtSignal(str)
    # create a signal for track status and controlling the MainWindow GUI
    track_status = pyqtSignal(int)

    client = mqtt.Client()
    settings: MQTTSettings

    def on_connect(self, client, userdata, flags, rc):

        self.settings = MQTTSettings.get_instance()

        if rc != 0:
            self.add_log_line.emit(_("Couldn't connect to MQTT Broker \"{0}\".").format(self.settings.hostname))
            self.track_status.emit(100)
            return rc

        self.add_log_line.emit(_("Connected to MQTT Broker \"{0}\" on port {1}.").format(self.settings.hostname,
                                                                                     self.settings.port))
        self.track_status.emit(101)

        try:
            client.subscribe(f"{self.settings.topic}/#")
            self.add_log_line.emit(_("Subscribing to topic \"{0}/#\".").format(self.settings.topic))
        except ValueError:
            self.add_log_line.emit(_("Couldn't subscribe to topic \"{0}/#\". You provided an invalid or emtpy topic.").
                                   format(self.settings.topic))
            self.track_status.emit(103)
        self.add_log_line.emit(_("Listening to Broker."))
        self.track_status.emit(300)

    def router(self, data):
        mqtt_command = data.get("command")
        mqtt_arg = data.get("args")

        if mqtt_command is not None:
            self.add_log_line.emit(_("Received command \"{0}\" with argument \"{1}\".").format(mqtt_command, mqtt_arg))

        command_to_run = find_command_to_run(mqtt_command, mqtt_arg)
        command_line_args = find_command_line_arguments(mqtt_command, mqtt_arg)

        if command_to_run is not None:
            # when there are spaces in the given command we should set it in quotes
            if ' ' in command_to_run:
                command_to_run = f"\"{command_to_run}\""

            self.add_log_line.emit(_("Executing command \"{0}\".").format(command_to_run))
            os.system(f"{command_to_run} {command_line_args}")
            self.add_log_line.emit(_("Command \"{0}\" was executed.").format(command_to_run))
        else:
            if mqtt_command is None:
                self.add_log_line.emit(
                    _("Couldn't read command from the MQTT payload. Ensure that you are sending a \"command\" attribute"
                      " in the MQTT payload.")
                    .format(mqtt_command))
            else:
                self.add_log_line.emit(_("Payload command \"{0}\" is not defined. Please add it via the Payload "
                                         "Handler tab.")
                                       .format(mqtt_command))
                self.track_status.emit(104)

    def on_message(self, client, userdata, msg):
        topic = msg.topic.replace(f"{self.settings.topic}/", "")
        data = extract_payload(msg.payload)
        self.add_log_line.emit(_("Received MQTT payload \"{0}\" via topic \"{1}\".").format(data, topic))
        self.router(data)

    def __init__(self):
        super().__init__()
        self.settings = MQTTSettings.get_instance()

    def run(self):
        self.mqtt_connect()

    def mqtt_connect(self):
        if self.settings.hostname is None or self.settings.port is None or self.settings.topic is None:
            return False

        self.client = mqtt.Client()

        if self.settings.hostname != "" and self.settings.port != "" and self.settings.topic != "":
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_log = self.mqtt_log
            self.client.username_pw_set(self.settings.username, self.settings.password)

            try:
                if self.settings.enable_ssl:
                    if self.settings.enable_client_ssl_auth:

                        if self.settings.client_certificate_file == "" or self.settings.client_key_file == "":
                            self.add_log_line.emit(_("You either didn't provide a client certificate or client key "
                                                     "file. Both are needed for SSL/TLS client certificate "
                                                     "authentication. Canceling."))
                            self.track_status.emit(301)
                            #self.mqtt_disconnect()
                            return False

                        self.client.tls_set(ca_certs=self.settings.server_certificate_file,
                                            certfile=self.settings.client_certificate_file,
                                            keyfile=self.settings.client_key_file,
                                            tls_version=ssl.PROTOCOL_TLSv1_2)
                    elif self.settings.allow_insecure_ssl and self.settings.server_certificate_file != "":
                        # disable checks for certificates and allow insecure TLS
                        self.client.tls_set(ca_certs=self.settings.server_certificate_file,
                                            tls_version=ssl.PROTOCOL_TLSv1_2)
                        self.client.tls_insecure_set(True)
                        # but warn the user, because this is not a recommended setup!
                        self.add_log_line.emit(_("WARNING: INSECURE SSL/TLS ENABLED! PROCEED WITH CAUTION!"))
                    elif self.settings.allow_insecure_ssl and self.settings.server_certificate_file == "":
                        # disable checks for certificates and allow insecure TLS
                        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
                        self.client.tls_insecure_set(True)
                        # but warn the user, because this is not a recommended setup!
                        self.add_log_line.emit(_("WARNING: INSECURE SSL/TLS ENABLED! PROCEED WITH CAUTION!"))
                    else:
                        # we just want in transit encryption
                        self.client.tls_set(ca_certs=self.settings.server_certificate_file,
                                            tls_version=ssl.PROTOCOL_TLSv1_2)

                self.client.connect(self.settings.hostname, int(self.settings.port), 60)
                self.client.loop_start()

            except ConnectionRefusedError:
                self.add_log_line.emit(_("Broker refused the connection. Did you maybe provide wrong credentials?"))
                return False
            except ValueError:
                return False
            except TimeoutError:
                return False
            except SSLError as e:
                if hasattr(e, 'message'):
                    self.add_log_line.emit(f"openSSL: {str(e.message)}")
                else:
                    self.add_log_line.emit(f"openSSL: {str(e)}")

                return False
            except ConnectionResetError:
                if self.settings.enable_ssl and self.settings.port == "1883":
                    self.add_log_line.emit(_("Broker has reset the connection. You are trying to connect using SSL/TLS "
                                             "on plaintext MQTT port 1883. Retry with port 8883!"))

                else:
                    self.add_log_line.emit(_("Connection reset by broker."))

                return False
        else:
            self.add_log_line.emit(_("MQTT Connection not set up. Please provide a Hostname, Port and Topic."))
            self.track_status.emit(200)

    def mqtt_log(self, client, userdata, level, buff):
        self.add_log_line.emit(f"paho-mqtt: {buff}")

    def mqtt_disconnect(self):
        self.add_log_line.emit(_("Disconnecting from Broker."))
        self.track_status.emit(301)
        self.client.loop_stop()
        try:
            self.client.disconnect()
        except SSLZeroReturnError:
            return
        self.add_log_line.emit(_("Disconnected from Broker."))
        self.track_status.emit(105)

    def mqtt_reconnect(self):
        self.mqtt_disconnect()
        self.add_log_line.emit(_("Reconnecting to Broker."))
        self.track_status.emit(302)
        self.mqtt_connect()

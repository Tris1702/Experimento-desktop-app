import threading
from paho.mqtt import client as mqtt_client
from datetime import datetime
from config.constance import Constance
import logging
from publish_data import DataFactory
from measure_data import MeasureData

class ClientMQTT:
    def __init__(self):
        self.BROKER = Constance.MQTT_BROKER
        self.PORT = Constance.MQTT_PORT
        self.CLIENT_ID =Constance.MQTT_CLIENT_ID
        self.USERNAME = Constance.MQTT_USERNAME
        self.PASSWORD = Constance.MQTT_PASSWORD
        self.FLAG_CONNECTED = False
        self.ADMIN_TOPIC = None
        self.COMMAND_TOPIC = None
        self.client = None
        self.timer_online = None

    def set_admin_topic(self, admin_topic: str) -> None:
        """
        Admin topic is topic where student send data to monitor website
        This topic must be similar to Room Code (which is create by teacher on monitor website)
        """
        self.ADMIN_TOPIC = admin_topic

    def set_command_topic(self, command_topic: str) -> None:
        """
        Command topic is topic where student's device received command from monitor website
        This topic is the student's username (which is should contain student'id)
        """
        self.COMMAND_TOPIC = command_topic

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
            self.client.subcriber(self.COMMAND_TOPIC)
            self.client.subcriber(self.ADMIN_TOPIC)
            self.publish_online()
            self.FLAG_CONNECTED = True
        else:
            logging.error('Failed to connect, return code {rc}.'.format(rc = rc))

    def on_disconnect(self, client, userdata, rc) -> None:
        self.timer_online.cancel()
        self.on_disconnect()

    def unsubcribe(self) -> None:
        self.client.unsubcribe(self.COMMAND_TOPIC)
        self.COMMAND_TOPIC = None

    def connect_mqtt(self) -> mqtt_client.Client:
        client = mqtt_client.Client(self.CLIENT_ID, transport=Constance.mqtt_transport)
        client.username_pw_set(self.USERNAME, self.PASSWORD)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect
        client.tls_set()
        client.connect(self.BROKER, self.PORT)
        return client

    def publish_command_topic(self) -> None:
        # Publish Command topic to Admin topic

        logging.info('Admin get all topics')
        msg = DataFactory.gen_return_topic_data(self.COMMAND_TOPIC)
        self.publish_data(self.ADMIN_TOPIC, msg)

    def publish_online(self) -> None:
        # Publish online status to monitor website

        self.timer_online = threading.Timer(5.0, self.publish_online)
        self.timer_online.start()
        msg = DataFactory.gen_online_status(self.COMMAND_TOPIC)
        self.publish_data(self.ADMIN_TOPIC, msg)

    def publish_history(self, data_type: str, command_topic: str, history_data: list[MeasureData]):
        # Publish measure history data

        logging.info('History')
        try:
            msg = DataFactory.gen_history_data(data_type, command_topic, history_data)
            self.publish_data(self.COMMAND_TOPIC, msg)
        except NameError:
            logging.error(NameError)

    def publish_data(self, target_topic: str, data: Any) -> None:
        #Publish data in general

        self.client.publish(target_topic, data)

    def on_message(self, client, userdata, msg):
        #Got message from topic

        payload = msg.payload.decode()
        topic = msg.topic
        try:
            logging.info(payload)
            data = json.loads(payload)
            type = data['type']
            if topic == self.ADMIN_TOPIC:
                logging.info(type)
                if type == Constance.GET_ALL_TOPIC:
                    self.public_command_topic()
            else:
                if type == Constance.GET_HISTORY_TOPIC:
                    message = data['message']
                    self.publish_history(message)
        except NameError:
            logging.error(NameError)


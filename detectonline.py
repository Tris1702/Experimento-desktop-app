# python 3.6

import json
import random
import time
import serial
import serial.tools.list_ports
import threading

from paho.mqtt import client as mqtt_client
from datetime import datetime

class DetectOnline:
    def __init__(self, history):
        self.BROKER = 'broker.emqx.io'
        # self.BROKER='broker.mqttdashboard.com'
        # self.BROKER = 'test.mosquitto.org'
        self.PORT = 8083
        self.CLIENT_ID = "python-mqtt-ws-pub-sub-{id}".format(id=random.randint(0, 1000))
        self.USERNAME = 'emqx'
        self.PASSWORD = 'public'
        self.FLAG_CONNECTED = 0
        self.TOPICADMIN='admin'
        self.history = history

    def set_topic(self, topic):
        self.TOPIC = topic 

    def on_connect(self, client, userdata, flags, rc):
        global FLAG_CONNECTED
        if rc == 0:
            FLAG_CONNECTED = 1
            print("Connected to MQTT Broker!")
            self.client.subscribe(self.TOPIC)
            self.client.subscribe(self.TOPICADMIN)
            self.public_online()
        else:
            print("Failed to connect, return code {rc}".format(rc=rc), )


    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        topic = msg.topic
        print(topic, self.TOPIC)
        try:
            print(payload)
            data = json.loads(payload)
            type = data['type']
            if ('data' in data):
                message = data['data']

            if topic == self.TOPICADMIN:
                print(type)
                if type == 'get-all-topic':
                    self.public_topic()
                elif type == 'get-history':
                    self.publish_history()
        except:
            print(payload)
        
    def unsubcribe(self):
        self.TOPIC = 'none'
        self.client.unsubscribe(self.TOPIC)

    def connect_mqtt(self):
        client = mqtt_client.Client(self.CLIENT_ID, transport='websockets')
        client.username_pw_set(self.USERNAME, self.PASSWORD)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect
        client.connect(self.BROKER, self.PORT)
        return client

    def on_disconnect(self,client, userdata, rc):
        self.timer_online.cancel()
        self.on_disconnect()
        

    
    def publish_history(self):
        try:
            msg_dict = {
                'type': 'return-history',
                'id': self.TOPIC,
                'data': [tmp for tmp in self.history if tmp['id'] == self.TOPIC][::-1] 
            }
            msg = json.dumps(msg_dict)
            self.client.publish(self.TOPICADMIN, msg)
            print(msg)
        except NameError:
            print(NameError)

    def public_topic(self):
        print("getalltopic")
        msg_dict = {
            'type': 'return-topic',
            'topicName': self.TOPIC
        }
        msg = json.dumps(msg_dict)
        self.client.publish(self.TOPICADMIN, msg)

    def public_online(self):
        self.timer_online = threading.Timer(5.0, self.public_online)
        self.timer_online.start()
        msg_dict = {
            'type': 'online',
            'id': self.TOPIC
        }
        msg = json.dumps(msg_dict)
        self.client.publish(self.TOPICADMIN, msg)

    def run(self):
        self.client = self.connect_mqtt()
        self.client.loop_start()
        time.sleep(1)
    
    # def deleteData(self, timeData):
    #     self.history = [element for element in self.history if element['data']['time'] == timeData]
    #     msg_dict = {
    #         'type': 'delete-single-data-by-id',
    #         'id': self.TOPIC,
    #         'data': {
    #             'time': timeData
    #         }
    #     }
    #     msg = json.dumps(msg_dict)
    #     self.client.publish(self.TOPIC, msg)

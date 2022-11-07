# python 3.6

import json
import random
import time
import serial
import serial.tools.list_ports
import threading

from paho.mqtt import client as mqtt_client
from datetime import datetime

class Detect:
    def __init__(self):
        # self.BROKER = 'broker.emqx.io'
        self.BROKER='broker.mqttdashboard.com'
        self.PORT = 8000
        self.CLIENT_ID = "python-mqtt-ws-pub-sub-{id}".format(id=random.randint(0, 1000))
        self.USERNAME = 'emqx'
        self.PASSWORD = 'public'
        self.FLAG_CONNECTED = 0
        self.history=[]
        self.TOPICADMIN='admin'
        self.subcribe('topicccccssss')
        self.run()
        self.set_serial_port('/dev/ttyACM0')

    def subcribe(self, topic):
        self.TOPIC = topic 

    def set_serial_port(self, serialPortName):
        self.SERIAL_PORT = serial.Serial(serialPortName, 9600)

    def get_coms(self):
        print('get com')
        ports = serial.tools.list_ports.comports()
        result = []
        for i in ports:
            result.append(str(i).split()[0])
        if len(result) == 0: result = ['No COM detected']
        return result

    def on_connect(self, client, userdata, flags, rc):
        global FLAG_CONNECTED
        if rc == 0:
            FLAG_CONNECTED = 1
            print("Connected to MQTT Broker!")
            self.client.subscribe(self.TOPIC)
            # self.client.subscribe(self.TOPICADMIN)
            # self.public_online()
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
                
            elif topic == self.TOPIC:
                if type == 'get-live-data':
                    distance = message['distance']
                    self.measure(distance)
                elif type == 'get-history':
                    self.publish_history()
        except:
            print(payload)
        
    def unsubcribe(self):
        self.TOPIC = 'none'
        self.client.unsubscribe(self.TOPIC)

    def connect_mqtt(self):
        client = mqtt_client.Client(self.CLIENT_ID, transport='websockets')
        # client.username_pw_set(self.USERNAME, self.PASSWORD)
        # client.on_connect = self.on_connect
        # client.on_message = self.on_message
        # client.on_disconnect = self.on_disconnect
        # client.connect(self.BROKER, self.PORT)
        return client

    def on_disconnect(self,client, userdata, rc):
        self.timer_online._stop()
        self.on_disconnect()
        

    def publish_data(self, distance):
        now = datetime.now()
        data = bytes("x", 'utf-8')
        self.SERIAL_PORT.write(data)
        res = self.SERIAL_PORT.readline()
        res = res.decode("utf-8").split(",")[0]
        
        msg_dict = {
            'type': 'live-data',
            'data': {
                'distance': distance,
                'voltage': res,
                'time': now.strftime("%H:%M:%S")
            }

        }
        # msg = json.dumps(msg_dict)
        print(msg_dict)
        # result = self.client.publish(self.TOPIC, msg)
        # status = result[0]
        # if status == 0:
        #     print("Send {msg} to topic {topic}".format(msg=msg, topic=self.TOPIC))
        #     self.history.append(msg_dict)
        # else:
        #     print("Failed to send message to topic {topic}".format(topic=self.TOPIC))

    #TODO: Not sure
    def publish_history(self):
        print("gethistory here")
        msg_dict = {
            'type': 'return-history',
            'id': self.TOPIC,
            'data': self.history
        }
        msg = json.dumps(msg_dict)
        self.client.publish(self.TOPIC, msg)

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
        # self.client.loop_start()
        time.sleep(1)
    
    def measure(self, message):
        if FLAG_CONNECTED:
            self.publish_data(message)
        else:
            self.client.loop_stop()
    
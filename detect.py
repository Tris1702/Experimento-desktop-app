# python 3.6

import json
import random
import time
import serial
import serial.tools.list_ports

from paho.mqtt import client as mqtt_client
from datetime import datetime

class Detect:
    def __init__(self):
        self.BROKER = 'broker.emqx.io'
        self.PORT = 8083
        self.CLIENT_ID = "python-mqtt-ws-pub-sub-{id}".format(id=random.randint(0, 1000))
        self.USERNAME = 'emqx'
        self.PASSWORD = 'public'
        self.FLAG_CONNECTED = 0
        self.history=[]

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
        return result

    def on_connect(self, client, userdata, flags, rc):
        global FLAG_CONNECTED
        if rc == 0:
            FLAG_CONNECTED = 1
            print("Connected to MQTT Broker!")
            client.subscribe(self.TOPIC)
        else:
            print("Failed to connect, return code {rc}".format(rc=rc), )


    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        try:
            data = json.loads(payload)
            type = data['type']
            message = data['message']
            print(type)
            if 'once' in type:
                self.measure(message)
            elif 'history' in type:
                self.send_history()
        except:
            print(payload)
        

    def connect_mqtt(self):
        client = mqtt_client.Client(self.CLIENT_ID, transport='websockets')
        client.username_pw_set(self.USERNAME, self.PASSWORD)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.BROKER, self.PORT)
        return client


    def publish(self, message):
        now = datetime.now()
        data = bytes("x", 'utf-8')
        self.SERIAL_PORT.write(data)
        res = self.SERIAL_PORT.readline()
        res = res.decode("utf-8").split(",")[0]
        msg_dict = {
            'dist': message,
            'number': res,
            'dateTime': now.strftime("%H:%M:%S")
        }
        msg = json.dumps(msg_dict)
        result = self.client.publish(self.TOPIC, msg)
        status = result[0]
        if status == 0:
            print("Send {msg} to topic {topic}".format(msg=msg, topic=self.TOPIC))
            self.history.append(msg)
        else:
            print("Failed to send message to topic {topic}".format(topic=self.TOPIC))

    def publish_history(self):
        self.client.publish(self.TOPIC, str(self.history))

    def run(self):
        self.client = self.connect_mqtt()
        self.client.loop_start()
        time.sleep(1)
    
    def measure(self, message):
        if FLAG_CONNECTED:
            self.publish(message)
        else:
            self.client.loop_stop()
    
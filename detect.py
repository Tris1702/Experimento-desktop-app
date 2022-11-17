# python 3.6

import json
import random
import time
import serial
import serial.tools.list_ports
import threading

from paho.mqtt import client as mqtt_client
from datetime import datetime

import websockets
from websocket import create_connection
import asyncio

class Detect():
    def __init__(self):
        self.CLIENT_ID = 11111
        self.FLAG_CONNECTED = 0
        self.history=[]
        self.TOPIC_ADMIN='admin'
        self.URL = "ws://192.168.1.101:4444"
        
    def run(self):
        asyncio.run(self.connect())
        
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

    async def connect(self):
        # Connect to the server
        global FLAG_CONNECTED
        async with websockets.connect(self.URL) as ws:
            FLAG_CONNECTED = 1
            self.WEBSOCKET = ws

            asyncio.run(self.sendMessage(self.TOPIC_ADMIN, 3, {})) 
            asyncio.run(self.sendMessage(self.TOPIC, 3, {}))
            asyncio.run(self.public_online())
            
            # Stay alive forever, listening to incoming msgs
            while True:
                payload = await ws.recv()
                data = json.loads(payload)
                type = data['type']
                topic = data['topic']
                
                if ('data' in data):
                    message = data['data']
                    
                if topic == self.TOPIC_ADMIN:
                    print(type)
                    if type == 'get-all-topic':
                        self.public_topic()
                elif topic == self.TOPIC:
                    if type == 'get-live-data':
                        distance = message['distance']
                        self.measure(distance)
                    elif type == 'get-history':
                        self.publish_history()
                    elif type == 'delete-single-data-by-id':
                        timeData = data['time']
                        self.delete_data_by_id(timeData)
                    
                
    async def sendMessage(self, topic, type, payload):
        msg_dict = {
            'clientId': self.CLIENT_ID,
            'topic': topic,
            'type': type,
            'payload': payload
        }
        msg = json.dumps(msg_dict)
        await self.WEBSOCKET.send(msg)

    def subcribe(self, topic):
        self.TOPIC = topic 
        
    async def unsubcribe(self):
        self.TOPIC = 'none'
        asyncio.run(self.sendMessage(self.TOPIC, 4, {}))
        
    async def public_topic(self):
        print("getalltopic")
        payload = {
            'type': 'return-topic',
            'topicName': self.TOPIC
        }
        asyncio.run(self.sendMessage(self.TOPIC_ADMIN, 2, payload))
        
    async def measure(self, message):
        if FLAG_CONNECTED:
            asyncio.run(self.sendMessage(self.TOPIC, 2, message))
 
    async def publish_history(self):
        try:
            payload = {
                'type': 'return-history',
                'id': self.TOPIC,
                'data': [tmp for tmp in self.history if tmp['id'] == self.TOPIC][::-1] 
            }
            asyncio.run(self.sendMessage(self.TOPIC, 2, payload))
        except NameError:
            print(NameError)
    
    async def public_online(self):
        self.timer_online = threading.Timer(5.0, self.public_online)
        self.timer_online.start()
        payload = {
            'type': 'online',
            'id': self.TOPIC
        }
        asyncio.run(self.sendMessage(self.TOPIC_ADMIN, 2, payload))
            
    async def delete_data_by_id(self, timeData):
        self.history = [element for element in self.history if element['data']['time'] == timeData]
        payload = {
            'type': 'return-delete-single-data-by-id',
            'id': self.TOPIC,
            'data': {
                'time': timeData
            }
        }
        asyncio.run(self.sendMessage(self.TOPIC, 2, payload))
    
        
class Detect3:
    def __init__(self):
        self.BROKER = 'localhost'
        # self.BROKER='broker.mqttdashboard.com'
        # self.BROKER = 'test.mosquitto.org'
        self.PORT = 4444
        self.CLIENT_ID = "111"
        self.USERNAME = 'emqx'
        self.PASSWORD = 'public'
        self.FLAG_CONNECTED = 0
        self.history=[]
        self.TOPICADMIN='admin'

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
                
            elif topic == self.TOPIC:
                if type == 'get-live-data':
                    distance = message['distance']
                    self.measure(distance)
                elif type == 'get-history':
                    self.publish_history()
                elif type == 'delete-single-data-by-id':
                    timeData = data['time']
                    self.delete_data_by_id(timeData)
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
        

    def publish_data(self, distance):
        now = datetime.now()
        data = bytes("x", 'utf-8')
        self.SERIAL_PORT.write(data)
        res = self.SERIAL_PORT.readline()
        res = res.decode("utf-8").split(",")[0]
        
        msg_dict = {
            'type': 'live-data',
            'id': self.TOPIC,
            'data': {
                'distance': distance,
                'voltage': res,
                'time': now.strftime("%H:%M:%S")
            }
        }
        msg = json.dumps(msg_dict)
        print(msg_dict)
        result = self.client.publish(self.TOPIC, msg)
        status = result[0]
        if status == 0:
            print("Send {msg} to topic {topic}".format(msg=msg, topic=self.TOPIC))
            self.history.append(msg_dict)
        else:
            print("Failed to send message to topic {topic}".format(topic=self.TOPIC))

    #TODO: Not sure
    def publish_history(self):
        try:
            msg_dict = {
                'type': 'return-history',
                'id': self.TOPIC,
                'data': [tmp for tmp in self.history if tmp['id'] == self.TOPIC][::-1] 
            }
            msg = json.dumps(msg_dict)
            self.client.publish(self.TOPIC, msg)
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
    
    def measure(self, message):
        if FLAG_CONNECTED:
            self.publish_data(message)
        else:
            self.client.loop_stop()
    
    def deleteData(self, timeData):
        self.history = [element for element in self.history if element['data']['time'] == timeData]
        msg_dict = {
            'type': 'return-delete-single-data-by-id',
            'id': self.TOPIC,
            'data': {
                'time': timeData
            }
        }
        msg = json.dumps(msg_dict)
        self.client.publish(self.TOPIC, msg)

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

            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            await self.sendMessage(self.TOPIC_ADMIN, 3, {})
            await self.sendMessage(self.TOPIC, 3, {})
            # self.public_online()
            
            # Stay alive forever, listening to incoming msgs
            while True:
                payload = await ws.recv()
                data = json.loads(payload)
                print(data)
                topic = data['topic']
                type = data['type']
                if ('data' in data):
                    message = data['data']
                print(topic)
                if topic == self.TOPIC_ADMIN:
                    print(type)
                    if type == 'get-all-topic':
                        self.public_topic()
                elif topic == self.TOPIC:
                    if type == 'get-live-data':
                        print("alo")
                        distance = message['distance']
                        await self.measure(distance)
                    elif type == 'get-history':
                        await self.publish_history()
                    elif type == 'delete-single-data-by-id':
                        timeData = data['time']
                        await self.delete_data_by_id(timeData)
                    
                
    async def sendMessage(self, topic, type, payload):
        print("send")
        new_payload = payload
        new_payload['topic'] = topic
        msg_dict = {
            'clientId': self.CLIENT_ID,
            'topic': topic,
            'type': type,
            'payload': new_payload
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
        
    async def measure(self, distance):
        if FLAG_CONNECTED:
            now = datetime.now()
            data = bytes("x", 'utf-8')
            self.SERIAL_PORT.write(data)
            res = self.SERIAL_PORT.readline()
            res = res.decode("utf-8").split(",")[0]
            
            payload = {
                'type': 'live-data',
                'id': self.TOPIC,
                'data': {
                    'distance': distance,
                    'voltage': res,
                    'time': now.strftime("%H:%M:%S")
                }
            }
            print(payload)
            await self.sendMessage(self.TOPIC,2 , payload)
            self.history.append(payload)
 
    async def publish_history(self):
        try:
            payload = {
                'type': 'return-history',
                'id': self.TOPIC,
                'data': [tmp for tmp in self.history if tmp['id'] == self.TOPIC][::-1] 
            }
            await self.sendMessage(self.TOPIC, 2, payload)
        except NameError:
            print(NameError)
    
    async def public_online(self):
        self.timer_online = threading.Timer(5.0, self.public_online)
        self.timer_online.start()
        payload = {
            'type': 'online',
            'id': self.TOPIC
        }
        await self.sendMessage(self.TOPIC_ADMIN, 2, payload)
            
    async def delete_data_by_id(self, timeData):
        self.history = [element for element in self.history if element['data']['time'] != timeData]
        payload = {
            'type': 'return-delete-single-data-by-id',
            'id': self.TOPIC,
            'data': {
                'time': timeData
            }
        }
        await self.sendMessage(self.TOPIC, 2, payload)\
        
    async def publish_data(self, distance):
        now = datetime.now()
        data = bytes("x", 'utf-8')
        self.SERIAL_PORT.write(data)
        res = self.SERIAL_PORT.readline()
        res = res.decode("utf-8").split(",")[0]
        
        payload = {
            'type': 'live-data',
            'id': self.TOPIC,
            'data': {
                'distance': distance,
                'voltage': res,
                'time': now.strftime("%H:%M:%S")
            }
        }
        print(payload)
        await self.sendMessage(self.TOPIC,2 , payload)
        
        
detect = Detect()
detect.set_serial_port("COM5")
detect.subcribe("AHA_B19DCCN123")
detect.run()
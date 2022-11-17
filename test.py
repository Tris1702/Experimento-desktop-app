import websockets
import asyncio
import json

# The main function that will handle connection and communication 
# with the server



class Detect():
    def __init__(self):
        self.CLIENT_ID = 111
        self.FLAG_CONNECTED = 0
        self.history=[]
        self.TOPICADMIN='admin'
  

    async def connect(self):
        url = "ws://192.168.1.101:4444"
        # Connect to the server
        async with websockets.connect(url) as ws:
            # Send a greeting message
            subInfo = {
                'clientId': 456,
                'topic': "AHA_B19DCCN123",
                'type': 3,
                'payload': {},
            }
            sub = json.dumps(subInfo)
            await ws.send(sub)
            self.WEBSOCKET = ws
            await self.sendMessage()
            # Stay alive forever, listening to incoming msgs
            test = ws 
            print(test)
            while True:
                msg = await ws.recv()
                print(msg)
                res = json.loads(msg)
                if res['type'] == 'get-live-data':
                    print ("send")
                    await self.sendMessage()
    
    async def sendMessage(self):
        msg_dict = {
            'clientId': 111,
            'topic': "AHA_B19DCCN123",
            'type': 2,
            'payload': {
                'type': 'online',
                'id': "alo123"
            }
        }
        msg = json.dumps(msg_dict)
        print(self.WEBSOCKET)
        await self.WEBSOCKET.send(msg)
    
    def run(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
        msg_dict = {
            'clientId': 111,
            'topic': "AHA_B19DCCN123",
            'type': 2,
            'payload': {
                'type': 'online',
                'id': "alo123"
            }
        }
        msg = json.dumps(msg_dict)
        print(self.WEBSOCKET)
        self.WEBSOCKET.send(msg)
        
detect = Detect()
detect.run()
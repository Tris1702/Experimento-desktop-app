import time
import serial
import serial.tools.list_ports
import threading
from datetime import datetime

class DetectOffline:
    def __init__(self):
        self.history=[]

    def set_serial_port(self, serialPortName):
        self.SERIAL_PORT = serial.Serial(serialPortName, 9600, write_timeout=0)
    
    def get_coms(self):
        print('get com')
        ports = serial.tools.list_ports.comports()
        result = []
        for i in ports:
            result.append(str(i).split()[0])
        if len(result) == 0: result = ['No COM detected']
        return result
    
    def add_data(self, distance):
        now = datetime.now()
        print(self.SERIAL_PORT)
        data = bytes("x", 'utf-8')
        self.SERIAL_PORT.write(data)
        print('Complete write')
        res = self.SERIAL_PORT.readlines()
        print('Complete read')
        # res = res.decode("utf-8").split(",")[0]
        
        # msg_dict = {
        #     'distance': distance,
        #     'voltage': res,
        #     'time': now.strftime("%H:%M:%S")
        # }
        # print(msg_dict)
        # self.history.append(msg_dict)

    def measure(self, distance):
        try:
            self.add_data(distance)
        except NameError:
            print(NameError)
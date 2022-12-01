import serial
import serial.tools.list_ports
from datetime import datetime
from constance import Constance

class DetectOffline:
    def __init__(self, option):
        self.SERIAL_PORT=None
        self.first_time = True
        self.option = option

    def set_serial_port(self, serialPortName):
        self.SERIAL_PORT = serial.Serial(serialPortName, 9600, timeout=0.2)
        if self.first_time == True:
            self.first_time = False
            self.add_data(distance=None, timer=0)
    
    def get_coms(self):
        print('get com')
        ports = serial.tools.list_ports.comports()
        result = []
        for i in ports:
            result.append(str(i).split()[0])
        if len(result) == 0: result = ['No COM detected']
        return result
    
    def add_data(self, distance, timer):
        now = datetime.now()
        data = bytes("x", 'utf-8')
        self.SERIAL_PORT.write(data)
        res = self.SERIAL_PORT.readline()
        res = res.decode("utf-8").split(",")[0]
        if len(res) == 0:
            self.SERIAL_PORT.write(data)
            res = self.SERIAL_PORT.readline()
            res = res.decode("utf-8").split(",")[0]
        
        if distance != None and res != None:
            if self.option == 0:
                msg_dict = {
                    'ampe': float(distance),
                    'voltage': float(res),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyAV.append(msg_dict)
            elif self.option == 1:
                msg_dict = {
                    'centimeter': float(distance),
                    'voltage': float(res),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyCV.append(msg_dict)
            else:
                msg_dict = {
                    'time': timer,
                    'voltage': float(res),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyTV.append(msg_dict)
            print(msg_dict)
            Constance.history.append(msg_dict)

    def measure(self, distance, timer = None):
        self.add_data(distance, timer)
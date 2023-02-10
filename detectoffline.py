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
    
    def add_data(self, distance, timer, port=None, Rvalue=None):
        now = datetime.now()
        data = bytes("x", 'utf-8')
        self.SERIAL_PORT.write(data)
        res = self.SERIAL_PORT.readline()
        if len(res) == 0:
            self.SERIAL_PORT.write(data)
            res = self.SERIAL_PORT.readline()
        res = res.decode("utf-8").replace("\r\n","")
        res = res.split(",")
        print(res)
        if port != None:
            res = res[port]
        
        if distance != None and res != None:
            if self.option == 0:
                msg_dict = {
                    'ampe': distance,
                    'voltage': float(res),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyAV.append(msg_dict)
            elif self.option == 1:
                msg_dict = {
                    'centimeter': distance,
                    'voltage': float(res),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyCV.append(msg_dict)
            elif self.option == 2:
                msg_dict = {
                    'timepoint': timer,
                    'voltage': float(res),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyTV.append(msg_dict)
            else:
                msg_dict = {
                    'ampe2': round(float(res[1])/Rvalue, 2),
                    'voltage1': float(res[0]),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyA2V1.append(msg_dict)
            print(msg_dict)
            Constance.history.append(msg_dict)

    def measure(self, distance, timer = None, port=None, Rvalue=None):
        self.add_data(distance, timer, port, Rvalue)
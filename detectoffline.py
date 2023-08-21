import serial
import serial.tools.list_ports
from datetime import datetime
from constance import Constance
import re

class DetectOffline:
    def __init__(self, option):
        self.SERIAL_PORT=None
        self.first_time = True
        self.option = option

    def set_serial_port(self, serialPortName):
        self.SERIAL_PORT = serial.Serial(serialPortName, 9600, timeout=0.05)
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
            elif self.option == 2 and distance != -1:
                if port == None:
                    msg_dict = {
                        'timepoint': timer,
                        'voltage1': float(res[0]),
                        'voltage2': float(res[1]),
                        'time': now.strftime("%H:%M:%S")
                    }
                    Constance.historyTVV.append(msg_dict)
                else:
                    msg_dict = {
                        'timepoint': timer,
                        'voltage': float(res),
                        'time': now.strftime("%H:%M:%S")
                    }
                    Constance.historyTV.append(msg_dict)
            elif self.option == 3:
                msg_dict = {
                    'ampe2': round(float(res[1])/Rvalue, 2),
                    'voltage1': float(res[0]),
                    'time': now.strftime("%H:%M:%S")
                }
                Constance.historyA2V1.append(msg_dict)
            elif self.option == 4:
                try:
                    print(Constance.formulaIP1[4:])
                    R1value = float(Constance.formulaIP1[4:])
                    operator1 = Constance.formulaIP1[3:4]

                    R2value = float(Constance.formulaIP2[4:])
                    operator2 = Constance.formulaIP2[3:4]

                    ampe1 = None
                    ampe2 = None

                    print(res[0])
                    if operator1 == '/':
                        ampe1 = round(float(res[0])/R1value, int(Constance.decimalPlacesIP1))
                    elif operator1 == '*':
                        ampe1 = round(float(res[0])*R1value, int(Constance.decimalPlacesIP1))
                    elif operator1 == '+':
                        ampe1 = round(float(res[0])+R1value, int(Constance.decimalPlacesIP1))
                    elif operator1 == '-':
                        ampe1 = round(float(res[0])-R1value, int(Constance.decimalPlacesIP1))
                        
                    if operator2 == '/':
                        ampe2 = round(float(res[1])/R2value, int(Constance.decimalPlacesIP2))
                    elif operator2 == '*':
                        ampe2 = round(float(res[1])*R2value, int(Constance.decimalPlacesIP2))
                    elif operator2 == '+':
                        ampe2 = round(float(res[1])+R2value, int(Constance.decimalPlacesIP2))
                    elif operator2 == '-':
                        ampe2 = round(float(res[1])-R2value, int(Constance.decimalPlacesIP2))
                    if ampe1 != None and ampe2 != None:
                        msg_dict = {
                            'ampe2': ampe2,
                            'ampe1': ampe1,
                            'time': now.strftime("%H:%M:%S")
                        }
                        Constance.historyI1I2.append(msg_dict)
                except:
                    return
            Constance.history.append(msg_dict)

    def measure(self, distance = 0, timer = None, port=None, Rvalue=None):
        self.add_data(distance, timer, port, Rvalue)
import serial
import serial.tools.list_ports as stlp
import numpy as np
from measure_data import MeasureData

class Detect:
    def __init__(self, option: str):
        self.option_detect = None
        self.serial_port = None
        self.first_time = True
        self.option = option
        self.list_coms = []
        self.measure_history = np.array([])

    def set_serial_port(self, serial_port: str) -> None:
        self.serial_port = serial_port.Serial(serial_port, 9600, timeout=0.2)
        if self.first_time:
            self.first_time = False
            self.get_measure_data()

    def get_coms(self) -> list[str]:
        ports = stlp.comports()
        for i in ports:
            self.list_coms.append(str(i).split()[0])
        if len(list_coms) == 0:
            self.list_coms = ['NO COM detected']
        return self.list_coms

    def measure(self, distance: float, source: str, timer: float = None) -> None:
        now = datetime.now()
        received_data = self.get_measure_data(timer)
        self.measure_history.append(MeasureData(time=now, type=self.option, data = received_data, source = source))

    def get_measure_data(self) -> list[float]:
        # Get data from coms after send to device 'x' character

        send_data = byte('x', 'utf-8')
        self.serial_port.write(send_data)
        received_data = self.serial_port.readline()
        received_data = received_data.decode('utf-8').split(',')
        if len(received_data) == 0:
            self.serial_port.write(data)
            received_data = self.serial_port.readline()
            received_data = received_data.decode('utf-8').split(',')
        return received_data

from control.controller_interface import ControllerInterface
from model.detect import Detect
from model.client_mqtt import ClientMQTT

class Controller(ControllerInterace):
    def __init__(self):
        self.detect = Detect()
        self.client = ClientMQTT()

    def reload_list_coms(self) -> list[str]:
        #Reload list coms
        return self.detect.get_coms()

    def measure_with_interval(self) -> None:
        #Measure continous with an interval time
        pass

    def draw_chart(self, option: str, draw_interpolation: bool) -> None:
        #From history data, draw them on chart
        pass

    def export_data(self) -> None:
        #Export data to excel file
        pass

    def measure(self, serial_port: str):
        if self.detect.serial_port is None:
            self.detect.set_serial_port(serial_port)
        self.detect.measure()
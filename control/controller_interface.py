import abc
class ControllerInterface(abc.ABC):
    @abc.abstractmethod
    def reload_list_coms(self) -> list[str]:
        #Reload list coms
        pass

    @abc.abstractmethod
    def measure_with_interval(self) -> None:
        #Measure continous with an interval time
        pass

    @abc.abstractmethod
    def draw_chart(self, option: str, draw_interpolation: bool) -> None:
        #From history data, draw them on chart
        pass

    @abc.abstractmethod
    def export_data(self) -> None:
        #Export data to excel file
        pass

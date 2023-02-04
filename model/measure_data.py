import typing
class MeasureData:
    def __init__(self, time: datetime, type: str, data: list[float], source: str):
        self.time = time
        self.type = type
        self.data = data
        self.source = source

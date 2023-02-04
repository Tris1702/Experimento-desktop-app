import logging
import json
from config.constance import Constance
from measure_data import MeasureData
class DataFactory:

    @staticmethod
    def gen_return_topic_data(topic_name: str) -> str:
        msg_dict = {
            'type': Constance.RETURN_TOPIC,
            'topicName': topic_name
        }
        msg = json.dumps(msg_dict)
        return msg

    @staticmethod
    def gen_online_status(target_topic: str) -> str:
        msg_dict = {
            'type': Constance.ONLINE_TOPIC,
            'id': target_topic
        }
        msg = json.dumps(msg_dict)
        return msg

    @staticmethod
    def gen_history_data(data_type: str, id: str, data: list[MeasureData]):
        msg_dict = {
            'data-type': data_type,
            'type': Constance.HISTORY_TOPIC,
            'id': id,
            'data': data
        }
        msg = json.dumps(msg_dict)
        return msg

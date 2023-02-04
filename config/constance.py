import random
class Constance:

    #MQTT Setting

    MQTT_TRANSPORT = 'websockets'
    MQTT_BROKER = 'broker.emqx.io'
    MQTT_PORT = 8084
    MQTT_CLIENT_ID =  "python-mqtt-ws-pub-sub-{id}".format(id=random.randint(0, 1000))
    MQTT_USERNAME = 'emqx'
    MQTT_PASSWORD = 'public'

    #Topic list
    RETURN_TOPIC = 'return-topic'
    HISTORY_TOPIC = 'return-history'
    ONLINE_TOPIC = 'online'

    GET_HISTORY_TOPIC = 'get-history'
    GET_ALL_TOPIC = 'get-all-topic'

import paho.mqtt.client as mqtt
from django.conf import settings
from gateway.settings import MQTT_CLIENT
import json

auto_flag = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("nodes/sensors/#", qos=MQTT_CLIENT["qos"])
        client.subscribe("nodes/actuators_modify/#", qos=MQTT_CLIENT["qos"])
        client.subscribe("nodes/authorize/#", qos=MQTT_CLIENT["qos"])
    else:
        print(f'Connection failed with code {rc}')

def on_message(client, userdata, message):
    from .models import Node, Sensor, Actuator, Data_Sensor, Data_Actuator
    from .automatic_actuators import control_actuator
    global auto_flag
    print("Received message:", message.payload.decode())
    # nodes/sensors/1
    if message.topic.startswith("nodes/sensors/"):
        node_id = int(message.topic.split("/")[-1])
        node = Node.objects.get(id=node_id)
        data = message.payload.decode()
        my_data = Data_Sensor(id=node)
        my_status = Sensor.objects.get(id=node)
        my_status.modify_status(node,data)
        if auto_flag == True:
            control_actuator(node_id, data)
    elif message.topic.startswith("nodes/actuators_modify/"):
        node_id = int(message.topic.split("/")[-1])
        node = Node.objects.get(id=node_id)
        data = message.payload.decode()
        my_data = Data_Actuator(id=node)
        my_status = Actuator.objects.get(id=node)
        my_status.modify_status(node,data)
    elif message.topic.startswith("nodes/authorize"):
        data = message.payload.decode()
        if data == "True":
            auto_flag = True
        elif data == "False":
            auto_flag = False
        print(auto_flag)

client = mqtt.Client(transport=MQTT_CLIENT["transport"], client_id=MQTT_CLIENT["client_id"])
client.on_connect = on_connect
client.on_message = on_message
client.ws_set_options(path=MQTT_CLIENT["path"])
client.username_pw_set(username=MQTT_CLIENT["username"], password=MQTT_CLIENT["password"])
client.connect(MQTT_CLIENT["host"], MQTT_CLIENT["port"], MQTT_CLIENT["keepalive"])

# data = {
#     "air_temperature_1": 25,
#     "air_temperature_2": 25,
#     "air_humidity_1": 50,
#     "air_humidity_2": 50,
#     "soil_moisture_1": 50,
#     "soil_moisture_2": 50,
#     "light_intensity_1": 243,
#     "light_intensity_2": 243,
# }

# node = Node.objects.get(id=1)
# my_data = Data_Sensor(id=node)
# for k,v in data.items():
#     setattr(my_data, k, v)
#     print(k, v)

# data = {
#     "motor_1": 1,
#     "motor_2": 1,
#     "motor_3": 0,
#     "motor_4": 1,
# }
from gateway.settings import MQTT_CLIENT
import json

MIN_TEMPERATURE = 20
MAX_TEMPERATURE = 25
MIN_SOIL_MOISTURE = 60
MAX_SOIL_MOISTURE = 80
MIN_LIGHT_INTENSITY = 2000
MAX_LIGHT_INTENSITY = 3000


def control_actuator(sensor_id, data):
    from .mqtt import client
    from .models import Node, Sensor, Actuator, Data_Sensor, Data_Actuator
    if data=="offline":
        return None
    Actuators = Actuator.objects.filter(relationship=sensor_id)
    print(Actuators)
    if not Actuators.exists():
        return None
    data = json.loads(data)
    for Actuator in Actuators:
        print(Actuator)
        if Actuator.status_node == True:
            print("Handle Actuator")
            data_send = {}
            if Actuator.status_motor_1 == True:
                if data['air_temperature_1'] is None and data['air_temperature_2'] is None:
                    data_send['motor_1'] = False
                else:
                    print("Handle Motor 1")
                    if data['air_temperature_1'] is None:
                        data['air_temperature_1'] = data['air_temperature_2']
                    if data['air_temperature_2'] is None:
                        data['air_temperature_2'] = data['air_temperature_1']
                    if (data['air_temperature_1'] + data['air_temperature_2']) / 2 > MAX_TEMPERATURE:
                        data_send['motor_1'] = True
                    elif (data['air_temperature_1'] + data['air_temperature_2']) / 2 < MIN_TEMPERATURE:
                        data_send['motor_1'] = False
            if Actuator.status_motor_2 == True:
                if data['soil_moisture_1'] is None and data['soil_moisture_2'] is None:
                    data_send['motor_2'] = False
                else:
                    print("Handle Motor 2")
                    if data['soil_moisture_1'] is None:
                        data['soil_moisture_1'] = data['soil_moisture_2']
                    if data['soil_moisture_2'] is None:
                        data['soil_moisture_2'] = data['soil_moisture_1']
                    if (data['soil_moisture_1'] + data['soil_moisture_2']) / 2 < MIN_SOIL_MOISTURE:
                        data_send['motor_2'] = True
                    elif (data['soil_moisture_1'] + data['soil_moisture_2']) / 2 > MAX_SOIL_MOISTURE:
                        data_send['motor_2'] = False
            if Actuator.status_motor_3 == True:
                if data['light_intensity_1'] is None and data['light_intensity_2'] is None:
                    data_send['motor_3'] = False
                else:
                    print("Handle Motor 3")
                    if data['light_intensity_1'] is None:
                        data['light_intensity_1'] = data['light_intensity_2']
                    if data['light_intensity_2'] is None:
                        data['light_intensity_2'] = data['light_intensity_1']
                    if (data['light_intensity_1'] + data['light_intensity_2']) / 2 < MIN_LIGHT_INTENSITY:
                        data_send['motor_3'] = True
                    elif (data['light_intensity_1'] + data['light_intensity_2']) / 2 > MAX_LIGHT_INTENSITY:
                        data_send['motor_3'] = False
            if data_send != {}:
                # Convert to JSON
                data_send = json.dumps(data_send)
                print(data_send)
                client.publish("nodes/actuators/" + str(Actuator.id), json.dumps(data_send), qos=MQTT_CLIENT['qos'])


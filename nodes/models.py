from django.db import models
import json

class Node(models.Model):
    id = models.AutoField(primary_key=True)
    feature = models.CharField(
        max_length=20,
        choices=(
            ('sensor', 'Sensor'),
            ('actuator', 'Actuator'),
        ),
        default=False,
    )

    def __str__(self):
        return f"Node {self.id}: {self.feature}"

    def get_data_latest(self):
        if self.feature == "sensor":
            status = Sensor.objects.values_list('status_node', 'status_air_temperature_1', 'status_air_temperature_2', 'status_air_humidity_1', 'status_air_humidity_2', 'status_soil_moisture_1', 'status_soil_moisture_2', 'status_light_intensity_1', 'status_light_intensity_2').get(id=self)
            # get data latest of sensor with get latest id_session
            data = Data_Sensor.objects.values_list('date_time', 'air_temperature_1', 'air_temperature_2', 'air_humidity_1', 'air_humidity_2', 'soil_moisture_1', 'soil_moisture_2', 'light_intensity_1', 'light_intensity_2').filter(id=self)
            if data.exists():
                data = data.latest('id_session')
            else:
                data = None
            return status, data
        elif self.feature == "actuator":
            status = Actuator.objects.values_list('status_node', 'status_motor_1', 'status_motor_2', 'status_motor_3', 'status_motor_4').get(id=self)
            # get data latest of actuator with get latest id_session
            data = Data_Actuator.objects.values_list('date_time', 'motor_1', 'motor_2', 'motor_3', 'motor_4').filter(id=self)
            if data.exists():
                data = data.latest('id_session')
            else:
                data = None
            return status, data

class Sensor(models.Model):
    id = models.OneToOneField(Node, on_delete=models.CASCADE, primary_key=True)
    status_node = models.BooleanField(null=True, default=False)
    relationship = models.IntegerField(null=True, default=-1)
    status_air_temperature_1 = models.BooleanField(null=True, default=False)
    status_air_temperature_2 = models.BooleanField(null=True, default=False)
    status_air_humidity_1 = models.BooleanField(null=True, default=False)
    status_air_humidity_2 = models.BooleanField(null=True, default=False)
    status_soil_moisture_1 = models.BooleanField(null=True, default=False)
    status_soil_moisture_2 = models.BooleanField(null=True, default=False)
    status_light_intensity_1 = models.BooleanField(null=True, default=False)
    status_light_intensity_2 = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f"{self.id} has ralationship with Node {self.relationship}"

    def modify_status(self, node, message):
        if message == "offline" or message == "Offline":
            self.status_node = False
            self.save()
            return
        data = json.loads(message)
        # Set all status in Sensor to False
        for k in self._meta.get_fields():
            if k.name.startswith('status_'):
                setattr(self, k.name, False)
        setattr(self, 'status_node', True)
        my_data = Data_Sensor(id=node)
        for k,v in data.items():
            setattr(self, f'status_{k}', True)
            setattr(my_data, k, v)
        my_data.save()
        self.save()



class Data_Sensor(models.Model):
    id_session = models.AutoField(primary_key=True)
    id = models.ForeignKey(Node, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    air_temperature_1 = models.FloatField(null=True, blank=True)
    air_temperature_2 = models.FloatField(null=True, blank=True)
    air_humidity_1 = models.FloatField(null=True, blank=True)
    air_humidity_2 = models.FloatField(null=True, blank=True)
    soil_moisture_1 = models.FloatField(null=True, blank=True)
    soil_moisture_2 = models.FloatField(null=True, blank=True)
    light_intensity_1 = models.FloatField(null=True, blank=True)
    light_intensity_2 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.date_time}"


class Actuator(models.Model):
    id = models.OneToOneField(Node, on_delete=models.CASCADE, primary_key=True)
    status_node = models.BooleanField(null=True, default=False)
    relationship = models.IntegerField(null=True, default=-1)
    status_motor_1 = models.BooleanField(null=True, default=False)
    name_motor_1 = models.CharField(default="Fan", max_length=30)
    status_motor_2 = models.BooleanField(null=True, default=False)
    name_motor_2 = models.CharField(default="Pump", max_length=30)
    status_motor_3 = models.BooleanField(null=True, default=False)
    name_motor_3 = models.CharField(default="Lamp", max_length=30)
    status_motor_4 = models.BooleanField(null=True, default=False)
    name_motor_4 = models.CharField(default="Motor 4", max_length=30)

    def __str__(self):
        return f"{self.id} has ralationship with Node {self.relationship}"

    def modify_status(self, node, message):
        if message == "offline":
            self.status_node = False
            self.save()
            return
        data = json.loads(message)
        # Set all status in Actuator to False
        for k in self._meta.get_fields():
            if k.name.startswith('status_'):
                setattr(self, k.name, False)
        setattr(self, 'status_node', True)
        my_data = Data_Actuator(id=node)
        for k,v in data.items():
            setattr(self, f'status_{k}', True)
            setattr(my_data, k, v)
        my_data.save()
        self.save()

class Data_Actuator(models.Model):
    id_session = models.AutoField(primary_key=True)
    id = models.ForeignKey(Node, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    motor_1 = models.BooleanField(null=True)
    motor_2 = models.BooleanField(null=True)
    motor_3 = models.BooleanField(null=True)
    motor_4 = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.id}: {self.date_time}"

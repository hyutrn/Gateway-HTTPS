from django.contrib import admin
from .models import Node, Sensor, Actuator, Data_Sensor, Data_Actuator

# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ("id", "feature")

admin.site.register(Node, NodeAdmin)

class SensorAdmin(admin.ModelAdmin):
    list_display = ("id", "status_node", "relationship", "status_air_temperature_1", "status_air_temperature_2", "status_air_humidity_1", "status_air_humidity_2", "status_soil_moisture_1", "status_soil_moisture_2", "status_light_intensity_1", "status_light_intensity_2")

admin.site.register(Sensor, SensorAdmin)

class ActuatorAdmin(admin.ModelAdmin):
    list_display = ("id", "status_node", "relationship", "status_motor_1", "name_motor_1", "status_motor_2", "name_motor_2", "status_motor_3", "name_motor_3", "status_motor_4", "name_motor_4")

admin.site.register(Actuator, ActuatorAdmin)

class Data_SensorAdmin(admin.ModelAdmin):
    list_display = ("id_session", "id", "date_time", "air_temperature_1", "air_temperature_2", "air_humidity_1", "air_humidity_2", "soil_moisture_1", "soil_moisture_2", "light_intensity_1", "light_intensity_2")

admin.site.register(Data_Sensor, Data_SensorAdmin)

class Data_ActuatorAdmin(admin.ModelAdmin):
    list_display = ("id_session", "id", "date_time", "motor_1", "motor_2", "motor_3", "motor_4")

admin.site.register(Data_Actuator, Data_ActuatorAdmin)

# Generated by Django 4.2.6 on 2024-01-02 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feature', models.CharField(choices=[('sensor', 'Sensor'), ('actuator', 'Actuator')], default=False, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Actuator',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nodes.node')),
                ('status_node', models.BooleanField(null=True)),
                ('relationship', models.IntegerField(default=-1, null=True)),
                ('status_motor_1', models.BooleanField(null=True)),
                ('name_motor_1', models.CharField(default='Motor 1', max_length=30)),
                ('status_motor_2', models.BooleanField(null=True)),
                ('name_motor_2', models.CharField(default='Motor 2', max_length=30)),
                ('status_motor_3', models.BooleanField(null=True)),
                ('name_motor_3', models.CharField(default='Motor 3', max_length=30)),
                ('status_motor_4', models.BooleanField(null=True)),
                ('name_motor_4', models.CharField(default='Motor 4', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nodes.node')),
                ('status_node', models.BooleanField(null=True)),
                ('relationship', models.IntegerField(default=-1, null=True)),
                ('status_air_temperature_1', models.BooleanField(null=True)),
                ('status_air_temperature_2', models.BooleanField(null=True)),
                ('status_air_humidity_1', models.BooleanField(null=True)),
                ('status_air_humidity_2', models.BooleanField(null=True)),
                ('status_soil_moisture_1', models.BooleanField(null=True)),
                ('status_soil_moisture_2', models.BooleanField(null=True)),
                ('status_light_intensity_1', models.BooleanField(null=True)),
                ('status_light_intensity_2', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Data_Sensor',
            fields=[
                ('id_session', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('air_temperature_1', models.FloatField(null=True)),
                ('air_temperature_2', models.FloatField(null=True)),
                ('air_humidity_1', models.FloatField(null=True)),
                ('air_humidity_2', models.FloatField(null=True)),
                ('soil_moisture_1', models.FloatField(null=True)),
                ('soil_moisture_2', models.FloatField(null=True)),
                ('light_intensity_1', models.FloatField(null=True)),
                ('light_intensity_2', models.FloatField(null=True)),
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nodes.node')),
            ],
        ),
        migrations.CreateModel(
            name='Data_Actuator',
            fields=[
                ('id_session', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('motor_1', models.BooleanField(null=True)),
                ('motor_2', models.BooleanField(null=True)),
                ('motor_3', models.BooleanField(null=True)),
                ('motor_4', models.BooleanField(null=True)),
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nodes.node')),
            ],
        ),
    ]

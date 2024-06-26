# Generated by Django 4.2.6 on 2024-01-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_alter_data_sensor_air_temperature_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_sensor',
            name='air_humidity_1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data_sensor',
            name='air_humidity_2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data_sensor',
            name='air_temperature_1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data_sensor',
            name='air_temperature_2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data_sensor',
            name='light_intensity_1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data_sensor',
            name='light_intensity_2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data_sensor',
            name='soil_moisture_1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data_sensor',
            name='soil_moisture_2',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

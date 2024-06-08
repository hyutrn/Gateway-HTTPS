Install package:

```

pip3 install -r requirements.txt

```

Run Server:

1. HTTP:
```
python3 manage.py runserver 0.0.0.0:8080
```
2. HTTPS(Choosing either option):
```
gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:8080 gateway.wsgi
```
Run MQTT Broker:
```
sudo mosquitto -v -c config_mqtt_broker.conf
```
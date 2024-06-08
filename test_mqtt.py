import paho.mqtt.client as mqtt
# Define MQTT broker settings
broker_address = "localhost"  # Replace with your WebSocket broker address if different
broker_port = 8083  # Default WebSocket port for MQTT
path = "/mqtt"

# Define client and callbacks

def on_connect(client, userdata, flags, rc):
   if rc == 0:
        print("Connected to broker")
        client.subscribe("#")
   else:
       print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, message):
   print("Received message:", message.payload.decode())

client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.ws_set_options(path="/mqtt")
client.username_pw_set(username="server", password="test")
client.connect(broker_address, broker_port)

# Start the network loop
client.loop_forever()


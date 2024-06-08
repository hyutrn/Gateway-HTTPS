from . import mqtt
import threading

thread = threading.Thread(target=mqtt.client.loop_start)
thread.start()
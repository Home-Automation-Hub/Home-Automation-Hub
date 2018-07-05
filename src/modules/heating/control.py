import mqtt
import time
from . import storage, websockets as ws
from multiprocessing import Process

def heating_on():
    mqtt.publish("flat/heating/hallway/chState", "on")
    storage.set("ch_running", True)

    ws.push_state()


def heating_off():
    mqtt.publish("flat/heating/hallway/chState", "off")
    storage.set("ch_running", False)

    ws.push_state()

def heating_set_on():
    mqtt.publish("flat/heating/hallway/sensorLed", "on")
    storage.set("ch_set_on", True)

    ws.push_state()

def heating_set_off():
    mqtt.publish("flat/heating/hallway/sensorLed", "off")
    storage.set("ch_set_on", False)

    heating_off() # This will also call ws.push_state()

def handle_temperature(topic, message):
    global temperature
    temperature = float(message)
    storage.set("temperature", temperature)

    ws.get_instance().publish("temperature", {
        "latest_reading": temperature
    })

def process_timer_management():
    while True:
        control_mode = storage.get("control_mode")
        print(control_mode)

        time.sleep(1)

def initialise(module_id):
    mqtt.subscribe("flat/heating/hallway/temperature", handle_temperature)
    Process(target=process_timer_management).start()

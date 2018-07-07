import mqtt
import time
from . import storage, websockets as ws
import threading
import datetime
import dateutil.parser

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
        now = datetime.datetime.now()
        control_mode = storage.get("control_mode")
        if control_mode == "manual":
            timing = storage.get("manual_control_timing")
            state = storage.get("manual_control_state")

            # If set to start at a specified time and currently waiting
            # until told to start 
            if timing.get("start") != "immediate" and state == "pending":
                start_timestamp = dateutil.parser.parse(timing.get("start"))
                if now > start_timestamp:
                    heating_set_on()
                    storage.set("manual_control_state", "running")

            if timing.get("end") != "indefinite" and state == "running":
                end_timestamp = dateutil.parser.parse(timing.get("end"))
                if now > end_timestamp:
                    heating_set_off()
                    storage.set("manual_control_state", "complete")
                

        time.sleep(1)

def initialise(module_id):
    mqtt.subscribe("flat/heating/hallway/temperature", handle_temperature)
    threading.Thread(target=process_timer_management).start()

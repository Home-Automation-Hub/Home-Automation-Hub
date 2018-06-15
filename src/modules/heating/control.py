import mqtt
from . import storage as _storage, websockets as ws

storage = None

def heating_on():
    mqtt.publish("flat/heating/hallway/chState", "on")
    storage.set("ch_is_on", True)

    ws.push_state()


def heating_off():
    mqtt.publish("flat/heating/hallway/chState", "off")
    storage.set("ch_is_on", False)

    ws.push_state()

def handle_temperature(topic, message):
    global temperature
    temperature = float(message)

    ws.get_instance().publish("temperature", {
        "latest_reading": temperature
    })

def initialise(module_id):
    global storage
    storage = _storage.get_instance()
    mqtt.subscribe("flat/heating/hallway/temperature", handle_temperature)
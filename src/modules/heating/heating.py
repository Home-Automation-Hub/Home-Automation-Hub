import mqtt
import math
import web
from storage import Storage

temperature = -1;

def module_http():
    response = ""
    response += web.get_request_method() + "<br>"
    response += str(web.get_request_form()) + "<br>"
    response += str(web.get_request_args()) + "<br>"
    response += str(temperature)

    return response


def control_heating(topic, message):
    global temperature
    temperature = float(message)
    print(f"Temperature: {temperature}")
    if math.isnan(temperature):
        return
    if temperature < 20:
        mqtt.publish("flat/heating/hallway/chState", "on")
    else:
        mqtt.publish("flat/heating/hallway/chState", "off")


def register(module_id):
    mqtt.subscribe("flat/heating/hallway/temperature", control_heating)
    web.add_endpoint("foo", module_http, ["GET", "POST"])

    storage = Storage(module_id)
    print(storage.get("test"))
    print(storage.set("test", "testing"))
    print(storage.get("test"))

import mqtt
import math
import web
from storage import ModuleStorage
from websocket import ModuleWebsocket
from flask import render_template, Blueprint

temperature = -1
ws = None
module_id = None
ch_is_on = None

# heating_bp = Blueprint("modules-heating", __name__, url_prefix="/modules/heating")

def module_http():
    return render_template("heating/index.html",
        ch_status = "On" if ch_is_on else "Off", temperature = temperature)

def module_http_bar():
    return "<h1>BAR</h1>"


def control_heating(topic, message):
    global temperature
    temperature = float(message)
    print(f"Temperature: {temperature}")

    ws.publish("temperature", {
        "latest_reading": temperature
    })

    if math.isnan(temperature):
        return
    if temperature < 20:
        mqtt.publish("flat/heating/hallway/chState", "on")
        ch_is_on = True
    else:
        mqtt.publish("flat/heating/hallway/chState", "off")
        ch_is_on = False


def register(module_id_):
    global ws, module_id
    module_id = module_id_

    mqtt.subscribe("flat/heating/hallway/temperature", control_heating)
    web.add_endpoint(module_id, "/", module_http, ["GET", "POST"])
    web.add_endpoint(module_id, "/bar/", module_http_bar, ["GET", "POST"])

    storage = ModuleStorage(module_id)
    print(storage.get("test"))
    print(storage.set("test", "testing"))
    print(storage.get("test"))
    ws = ModuleWebsocket(module_id)

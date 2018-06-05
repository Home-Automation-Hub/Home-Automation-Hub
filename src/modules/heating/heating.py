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

def module_http():
    return render_template("heating/index.html", ch_is_on=ch_is_on,
                           temperature=temperature)

def module_timers():
    return render_template("heating/timers.html")

def toggle_heating():
    if ch_is_on:
        heating_off()
    else:
        heating_on()

    return ""


def heating_on():
    global ch_is_on

    mqtt.publish("flat/heating/hallway/chState", "on")
    ch_is_on = True

    ws_push_state()


def heating_off():
    global ch_is_on

    mqtt.publish("flat/heating/hallway/chState", "off")
    ch_is_on = False

    ws_push_state()


def handle_temperature(topic, message):
    global temperature
    temperature = float(message)

    ws.publish("temperature", {
        "latest_reading": temperature
    })


def ws_push_state():
    ws.publish("state", {
        "ch_is_on": ch_is_on
    })


def register(module_id_):
    global ws, module_id
    module_id = module_id_

    mqtt.subscribe("flat/heating/hallway/temperature", handle_temperature)

    web.add_endpoint(module_id, "/", module_http, ["GET"])
    web.add_endpoint(module_id, "/timers/", module_timers, ["GET"])
    web.add_endpoint(module_id, "/action/toggle_heating/", toggle_heating, ["POST"])

    storage = ModuleStorage(module_id)
    print(storage.get("test"))
    print(storage.set("test", "testing"))
    print(storage.get("test"))
    ws = ModuleWebsocket(module_id)

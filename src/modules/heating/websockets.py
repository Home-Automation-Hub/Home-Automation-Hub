from websocket import ModuleWebsocket
from . import storage

ws = None

def get_instance():
    if not ws:
        raise Exception("Websocket not initialised")
    return ws

def push_state():
    print(storage.get("ch_is_on"))
    ws.publish("state", {
        "ch_is_on": storage.get("ch_is_on")
    })

def initialise(module_id):
    global ws, storage
    ws = ModuleWebsocket(module_id)    
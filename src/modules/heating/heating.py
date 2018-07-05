import mqtt
import math
from flask import render_template, Blueprint
from . import storage, websockets, control, web

def register(module_id_):
    module_id = module_id_

    storage.initialise(module_id)
    websockets.initialise(module_id)
    web.initialise(module_id)
    control.initialise(module_id)

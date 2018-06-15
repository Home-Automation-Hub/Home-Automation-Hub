import web
from .control import heating_on, heating_off
from flask import render_template
from . import storage

def view_index():
    ch_is_on=storage.get("ch_is_on")
    temperature=23

    return render_template("heating/index.html", ch_is_on=ch_is_on,
                           temperature=temperature)

def view_timers():
    return render_template("heating/timers.html")

def action_toggle_heating():
    ch_is_on=storage.get("ch_is_on")
    if ch_is_on:
        heating_off()
    else:
        heating_on()

    return ""

def initialise(module_id):
    web.add_endpoint(module_id, "/", view_index, ["GET"])
    web.add_endpoint(module_id, "/timers/", view_timers, ["GET"])
    web.add_endpoint(module_id, "/action/toggle_heating/",
            action_toggle_heating, ["POST"])
import web
from .control import heating_on, heating_off
from flask import render_template, request, jsonify
from . import storage, websockets as ws
from uuid import uuid4
import re
import json

def view_index():
    ch_is_on=storage.get("ch_is_on")
    temperature=23

    return render_template("heating/index.html", ch_is_on=ch_is_on,
                           temperature=temperature)

def view_timers():
    stor = storage.get_instance()
    timers = stor.get("timers") or []

    # Append a false "timer" which will prompt jinja to wrap it in
    # the approprate tags to be used as a template for adding new timers
    # in the frontend.  An empty dictionary for days also needs to be
    # added to prevent erors when we try and access entries of it for
    # the template row
    timers.append({"isTemplate": True, "days": {}})

    return render_template("heating/timers.html", timers=timers)

def action_toggle_heating():
    ch_is_on=storage.get("ch_is_on")
    if ch_is_on:
        heating_off()
    else:
        heating_on()

    return ""

def action_save_timers():
    timers = request.get_json()
    
    error = None

    time_re = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
    for timer in timers:
        # Validate that times are provided in a valid format
        if time_re.match(timer["startTime"]) == None or \
                time_re.match(timer["endTime"]) == None:
            error = "Start and end times must be of the format HH:MM"

        # Validate that the temperature is a floating point number
        try:
            float(timer["temperature"])
        except ValueError:
            error = "Temperature must be a number"

        # Validate that we have data for all 7 days and that each day is
        # either enabled or disabled
        supplied_days = set(timer["days"].keys())
        day_enabled_states = list(timer["days"].values())
        if supplied_days != set(["0","1","2","3","4","5","6"]):
            error = "All days must be supplied (either enabled or disabled)"
        for state in day_enabled_states:
            if state != True and state != False:
                error = "Day states must be a boolean"

    if error:
        return jsonify({"success": False, "message": error})        

    stor = storage.get_instance()
    stor.set("timers", timers)

    # Generate a random "modification ID" and send it with both the 
    # response and the websocket push.  This is used by the frontend to
    # ensure that the "timers have been modified" message is not shown
    # to the page which the timers were saved from.
    modification_id = str(uuid4())

    ws.get_instance().publish("timersModified", {
        "modification_id": modification_id
    })

    return jsonify({
        "success": True,
        "message": "Timers saved successfully",
        "modification_id": modification_id
    })


def initialise(module_id):
    web.add_endpoint(module_id, "/", view_index, ["GET"])
    web.add_endpoint(module_id, "/timers/", view_timers, ["GET"])
    web.add_endpoint(module_id, "/action/toggle_heating/",
            action_toggle_heating, ["POST"])
    web.add_endpoint(module_id, "/action/save_timers/",
            action_save_timers, ["POST"])
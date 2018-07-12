import web
from flask import render_template, request, jsonify
from . import storage, control, websockets as ws
from uuid import uuid4
import re
import json
import datetime
import dateutil.parser

def view_index():
    ch_is_on=storage.get("ch_is_on")
    control_mode=storage.get("control_mode")
    temperature=storage.get("temperature")
    thermostat_temperature = float(storage.get("thermostat_temperature"))
    
    manual_control_state, manual_state_message = \
            control.generate_manual_state_message()

    return render_template("heating/index.html", ch_is_on=ch_is_on,
                           temperature=temperature, control_mode=control_mode,
                           manual_control_state=manual_control_state,
                           manual_state_message=manual_state_message,
                           thermostat_temperature=thermostat_temperature)

def view_settings():
    num_readings_average = storage.get("num_readings_average")
    thermostat_delta_below = storage.get("thermostat_delta_below")
    thermostat_delta_above = storage.get("thermostat_delta_above")
    return render_template("heating/settings.html",
            num_readings_average=num_readings_average,
            thermostat_delta_below=thermostat_delta_below,
            thermostat_delta_above=thermostat_delta_above
        )

def view_timers():
    timers = storage.get("timers") or []

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
        control.heating_off()
    else:
        control.heating_on()

    return ""

def action_save_control_mode():
    request_data = request.get_json()
    control_mode = request_data.get("mode")

    if control_mode not in ["timer", "manual"]:
        return jsonify({"success": False, "message": "Invalid control mode"})

    storage.set("control_mode", control_mode)

    ws.get_instance().publish("controlModeModified", {
        "control_mode": control_mode
    })

    return jsonify({"success": True})


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

    storage.set("timers", timers)

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

def action_store_manual_control():
    control_options = request.get_json()
    start_time_type = control_options.get("startTimeType")
    start_time = control_options.get("startTime")
    end_time_type = control_options.get("endTimeType")
    end_time = control_options.get("endTime")
    
    error = None

    if start_time_type not in ["at", "now"]:
        error = "Start time type must be either 'at' or 'now'"

    if end_time_type not in ["until", "indefinitely"]:
        error = "End time type must be either 'until' or 'indefinitely'"

    time_re = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
    if start_time_type == "at":
        if time_re.match(start_time) == None:
            error = "Start time must be of the format HH:MM"

    if end_time_type == "until":
        if time_re.match(end_time) == None:
            error = "End time must be of the format HH:MM"

    if error:
        return jsonify({"success": False, "message": error})

    # Interpret the start and end times as dates.  If the a time has
    # already passed today, treat it as starting tomorrow. If the end
    # falls before the start, treat is ending on that time the day after
    # it has started.

    now = datetime.datetime.now()
    # Set to now to allow the calculation for end timestamp to work
    # when scheduled for immediate start
    start_dt = now
    if start_time_type == "at":
        start_dt = datetime.datetime.strptime(start_time, "%H:%M")
        start_dt = start_dt.replace(day=now.day, month=now.month, year=now.year)
        # If datetime is in the past then interpret as meaning tomorrow
        if start_dt < now:
            start_dt = start_dt + datetime.timedelta(days=1)

    end_dt = None
    if end_time_type == "until":
        end_dt = datetime.datetime.strptime(end_time, "%H:%M")
        end_dt = end_dt.replace(day=now.day, month=now.month, year=now.year)
        # Keep adding days until end falls after start
        while end_dt < start_dt:
            end_dt = end_dt + datetime.timedelta(days=1)

    start = start_dt.isoformat() if start_time_type == "at" else "immediate"
    end = end_dt.isoformat() if end_time_type == "until" else "indefinite"

    storage.set("manual_control_timing", {
        "start": start,
        "end": end
    })

    if start_time_type == "now":
        storage.set("manual_control_state", "running")
        control.heating_set_on()
    else:
        storage.set("manual_control_state", "pending")
        control.heating_set_off()

    state, message = control.generate_manual_state_message()
    ws.get_instance().publish("index_manual_message", {
        "state": state,
        "message": message
    })

    return jsonify({
        "success": True,
        "message": "Manual control saved successfully"
    })

def action_save_settings():
    control_options = request.get_json()
    num_readings_average = control_options.get("numReadingsAverage")
    thermostat_delta_below = control_options.get("thermostatDeltaBelow")
    thermostat_delta_above = control_options.get("thermostatDeltaAbove")

    try:
        num_readings_average = int(num_readings_average)
    except ValueError:
        return jsonify({
            "success": False,
            "message": ("Value for the following fields must be integers: \n"
                "\nNumber of readings in temperature average")
        })

    try:
        thermostat_delta_below = float(thermostat_delta_below)
        thermostat_delta_above = float(thermostat_delta_above)
    except ValueError:
        return jsonify({
            "success": False,
            "message": ("Value for the following fields must be floats: \n"
                "\nThermostat Temperature Deltas")
        })

    if num_readings_average < 1:
        return jsonify({
            "success": False,
            "message": ("Value for average number of readings must be greater "
                    "than 1")
        })
    
    storage.set("num_readings_average", num_readings_average)
    storage.set("thermostat_delta_below", thermostat_delta_below)
    storage.set("thermostat_delta_above", thermostat_delta_above)

    return jsonify({
        "success": True,
        "message": "Settings saved successfully!"
    })

def action_cancel_manual_operation():
    control.heating_set_off()
    storage.set("manual_control_state", "complete")
    control.update_manual_control_message()

    return jsonify({"success": True})

def action_change_thermostat(direction):
    change_value = 0.5
    if direction == "decrement":
        change_value = -0.5

    value = storage.get("thermostat_temperature")
    value += change_value
    storage.set("thermostat_temperature", value)

    ws.get_instance().publish("thermostat_updated", {
        "value": value
    })

    return jsonify({"success": True})

def initialise(module_id):
    web.add_endpoint(module_id, "/", view_index, ["GET"])
    web.add_endpoint(module_id, "/timers/", view_timers, ["GET"])
    web.add_endpoint(module_id, "/settings/", view_settings, ["GET"])
    web.add_endpoint(module_id, "/action/toggle_heating/",
            action_toggle_heating, ["POST"])
    web.add_endpoint(module_id, "/action/save_timers/",
            action_save_timers, ["POST"])
    web.add_endpoint(module_id, "/action/save_control_mode/",
            action_save_control_mode, ["POST"])
    web.add_endpoint(module_id, "/action/store_manual_control/",
            action_store_manual_control, ["POST"])
    web.add_endpoint(module_id, "/action/save_settings/",
            action_save_settings, ["POST"])
    web.add_endpoint(module_id, "/action/cancel_manual_operation/",
            action_cancel_manual_operation, ["POST"])
    web.add_endpoint(module_id, "/action/change_thermostat/<direction>/",
            action_change_thermostat, ["POST"])
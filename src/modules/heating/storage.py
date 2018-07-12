from storage import ModuleStorage

instance = None

def get_instance():
    if not instance:
        raise Exception("Storage instance not initialised")
    return instance

def set_default_values():
    instance.set("ch_is_on", False)

    default_values = {
        # How many temperature readings we average to calculate the current
        # temperature
        "num_readings_average": 6,
        # How far above the set temperature the environment must be
        # before thermostat turns heating off
        "thermostat_delta_above": 0.5,
        # How far below the set temperature the environment must be
        # before thermostat turns heating on
        "thermostat_delta_below": 0.5,
        "thermostat_temperature": 21,

    }

    for key in default_values:
        value = default_values[key]
        if not instance.get(key):
            instance.set(key, value)

    
    instance.redis.delete(instance.prefixed_key("temp_readings"))
    instance.redis.delete(instance.prefixed_key("temperature"))

def set(key, value):
    return instance.set(key, value)

def get(key):
    return instance.get(key)

def initialise(module_id):
    global instance
    instance = ModuleStorage(module_id)
    set_default_values()

def store_temperature_reading(reading):
    key = instance.prefixed_key("temp_readings")
    num_readings_average = instance.get("num_readings_average")
    instance.redis.lpush(key, float(reading))
    instance.redis.ltrim(key, 0, num_readings_average - 1)

def get_temperature_readings():
    readings = instance.redis.lrange(instance.prefixed_key("temp_readings"), 0,
            instance.get("num_readings_average") - 1)

    return [float(x) for x in readings]
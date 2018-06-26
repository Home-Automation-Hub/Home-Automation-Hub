from storage import ModuleStorage

instance = None

def get_instance():
    if not instance:
        raise Exception("Storage instance not initialised")
    return instance

def set_default_values():
    instance.set("ch_is_on", False)

def set(key, value):
    return instance.set(key, value)

def get(key):
    return instance.get(key)

def initialise(module_id):
    global instance
    instance = ModuleStorage(module_id)
    set_default_values()
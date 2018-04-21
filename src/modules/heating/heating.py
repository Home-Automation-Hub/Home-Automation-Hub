import mqtt
import math
import web

temperature = -1;


def module_http():
    return "Hello from module" + str(temperature)


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


def register():
    mqtt.subscribe("flat/heating/hallway/temperature", control_heating)
    web.add_endpoint("foo", module_http)

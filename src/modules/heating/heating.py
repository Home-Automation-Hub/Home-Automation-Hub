import mqtt
import math

def control_heating(topic, message):
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
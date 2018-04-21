from modules.heating import say_hello
import mqtt
import time

def main():
    def subscibe_to_topics():
        mqtt.subscribe("flat/heating/hallway/temperature", lambda t, m: print(f"Temperature: {m}"))
        mqtt.subscribe("flat/heating/hallway/humidity", lambda t, m: print(f"Humidity: {m}"))
        mqtt.subscribe("flat/heating/hallway/+", lambda t, m: print(f"Reading: {t} - {m}"))

    mqtt.set_up("10.114.1.101", 1883, subscibe_to_topics)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
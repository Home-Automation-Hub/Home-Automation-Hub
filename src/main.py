import mqtt
import time
import config

def main():
    def subscibe_to_topics():
        for module in config.enabled_modules:
            module.register()

    mqtt.set_up(config.mqtt_broker.get("host"), config.mqtt_broker.get("port"), subscibe_to_topics)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
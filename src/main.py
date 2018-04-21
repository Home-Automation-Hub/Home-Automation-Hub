import mqtt
from config import config
import web


def main():
    mqtt.set_up(config.mqtt_broker.get("host"), config.mqtt_broker.get("port"), register_modules)
    web.run()


def register_modules():
    for module in config.enabled_modules:
        web.endpoint_register_path_prefix = module["url_prefix"]
        module["module"].register()


if __name__ == "__main__":
    main()
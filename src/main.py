import mqtt
from config import config
import web
import storage
import websocket


def main():
    storage.set_up(config.redis_config.get("host"), config.redis_config.get("port"), config.redis_config.get("db"))
    mqtt.set_up(config.mqtt_broker.get("host"), config.mqtt_broker.get("port"), register_modules)
    websocket.start_server(config)
    web.run()


def register_modules():
    for module_id in config.enabled_modules:
        module = config.enabled_modules[module_id]
        module["module"].register(module_id)
        web.enabled_modules.append({
            "title": module["title"],
            "url_prefix": module["url_prefix"],
            "fontawesome_icon_class": module["fontawesome_icon_class"]
        })
    web.register_all_endpoints()


if __name__ == "__main__":
    main()
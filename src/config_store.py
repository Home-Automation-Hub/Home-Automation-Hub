import uuid


class ConfigStore():
    mqtt_broker = None
    enabled_modules = {}
    redis_config = None

    def set_mqtt_broker(self, host, port):
        self.mqtt_broker = {
            "host": host,
            "port": port
        }

    def register_module(self, module, url_prefix, title, storage_prefix):
        print("Registering module: " + str(module.__name__))
        self.enabled_modules[str(uuid.uuid4())] = {
            "module": module,
            "url_prefix": url_prefix,
            "title": title,
            "storage_prefix": storage_prefix
        }

    def set_redis_config(self, host, port, db):
        self.redis_config = {
            "host": host,
            "port": port,
            "db": db
        }

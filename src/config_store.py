class ConfigStore():
    mqtt_broker = None
    enabled_modules = []

    def set_mqtt_broker(self, host, port):
        self.mqtt_broker = {
            "host": host,
            "port": port
        }

    def register_module(self, module, url_prefix, title):
        self.enabled_modules.append({
            "module": module,
            "url_prefix": url_prefix,
            "title": title
        })
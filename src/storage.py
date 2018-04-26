import redis
import config

_instance = None


def set_up(host, port, db):
    global _instance, _config
    _instance = redis.StrictRedis(host=host, port=port, db=db)


class Storage():
    def __init__(self, module_id):
        self.key_prefix = "module:" + config.config.enabled_modules[module_id]["storage_prefix"]

    @property
    def redis(self):
        return _instance

    def prefixed_key(self, key):
        return f"{self.key_prefix}:{key}"

    def get(self, key):
        return _instance.get(self.prefixed_key(key))

    def set(self, key, value):
        return _instance.set(self.prefixed_key(key), value)


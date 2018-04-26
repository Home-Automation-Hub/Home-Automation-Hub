import redis
import config

redis_instance = None


def set_up(host, port, db):
    global redis_instance
    redis_instance = redis.StrictRedis(host=host, port=port, db=db)


class ModuleStorage():
    def __init__(self, module_id):
        self.key_prefix = "module:" + config.config.enabled_modules[module_id]["storage_prefix"]

    @property
    def redis(self):
        return redis_instance

    def prefixed_key(self, key):
        return f"{self.key_prefix}:{key}"

    def get(self, key):
        return redis_instance.get(self.prefixed_key(key))

    def set(self, key, value):
        return redis_instance.set(self.prefixed_key(key), value)


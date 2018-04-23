import redis
import config

_instance = None


def set_up(host, port, db):
    global _instance, _config
    _instance = redis.StrictRedis(host=host, port=port, db=db)


class Storage():
    def __init__(self, module_id):
        self.key_prefix = config.config.enabled_modules[module_id]["storage_prefix"]

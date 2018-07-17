from .config_store import ConfigStore
import home_automation_heating

config = ConfigStore()

config.register_module(home_automation_heating, "heating", "Central Heating",
        "heating", fontawesome_icon_class="thermometer-half")

config.set_mqtt_broker("mqtt", 1883)

config.set_redis_config("redis", 6379, 0)
from config_store import ConfigStore
import home_automation.heating

config = ConfigStore()

config.register_module(home_automation.heating, "heating", "Central Heating",
        "heating", fontawesome_icon_class="thermometer-half")

config.set_mqtt_broker("localhost", 1883)

config.set_redis_config("localhost", 6379, 0)
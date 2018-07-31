from .config_store import ConfigStore
import home_automation_heating
import home_automation_influxdb_logger

config = ConfigStore()
config.register_module(home_automation_heating, "heating", "Central Heating",
        "heating", fontawesome_icon_class="thermometer-half")
config.register_module(home_automation_influxdb_logger, "influxdb_logger",
        "InfluxDB Logger", "influxdb_logger",
        fontawesome_icon_class="database")

config.set_mqtt_broker("mqtt", 1883)

config.set_redis_config("redis", 6379, 0)
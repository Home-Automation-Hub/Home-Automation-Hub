from config_store import ConfigStore
from modules import heating

config = ConfigStore()

config.register_module(heating, "heating", "Central Heating")

config.set_mqtt_broker("10.114.1.101", 1883)

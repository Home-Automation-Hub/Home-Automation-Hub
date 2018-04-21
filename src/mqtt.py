from paho.mqtt.client import Client, topic_matches_sub

_instance = None
_subscribe_to_topics_func = None
_topic_callbacks = {}

def get_instance():
    return _instance


def _on_connect(client, userdata, flags, rc):
    _subscribe_to_topics_func()


def _on_message(client, userdata, message):
    callbacks_to_run = []
    for sub in _topic_callbacks.keys():
        if topic_matches_sub(sub, message.topic):
            callbacks_to_run += _topic_callbacks[sub]

    for callback in callbacks_to_run:
        callback(message.topic, message.payload)



def subscribe(topic, callback):
    if topic not in _topic_callbacks:
        _topic_callbacks[topic] = []
    _topic_callbacks[topic].append(callback)
    _instance.subscribe(topic)

def publish(topic, message):
    _instance.publish(topic, message)

def set_up(host, port, subscribe_to_topics_func):
    global _instance, _subscribe_to_topics_func
    _subscribe_to_topics_func = subscribe_to_topics_func
    _instance = Client()
    _instance.on_connect = _on_connect
    _instance.on_message = _on_message
    _instance.connect(host, port)
    _instance.loop_start()
from paho.mqtt.client import Client, topic_matches_sub
import threading
import uuid

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
            callbacks_to_run += list(_topic_callbacks[sub].values())

    for callback in callbacks_to_run:
        threading.Thread(target=callback, args=(message.topic, message.payload)).start()

def subscribe(topic, callback):
    if topic not in _topic_callbacks:
        _topic_callbacks[topic] = {}
    subscription_id = str(uuid.uuid4())
    _topic_callbacks[topic][subscription_id] = callback
    _instance.subscribe(topic)
    
    return (topic, subscription_id)

def unsubscribe(subscription_id_tuple):
    topic, subscription_id = subscription_id_tuple
    del _topic_callbacks[topic][subscription_id]

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
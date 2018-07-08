import websockets
import asyncio
import threading
import aioredis
import storage
import uuid
import json

redis_connection_host = None
redis_connection_db = None
redis_pool = None


async def socket_handler(websocket, path):
    global redis_pool

    if not redis_pool:
        redis_pool = await aioredis.create_pool(address=redis_connection_host,
                db=redis_connection_db)

    auth_key = await websocket.recv()

    redis_key = f"ws:auth:{auth_key}"
    auth_key_valid = storage.redis_instance.get(redis_key)
    storage.redis_instance.delete(redis_key)
    if not auth_key_valid:
        await websocket.send("invalid_auth")
        return

    await websocket.send("ok")

    channel = aioredis.Channel("websocket", is_pattern=False)
    redis_pool.execute_pubsub("subscribe", channel)
    try:
        while True:
            message = await channel.get()
            if message:
                await websocket.send(message.decode("UTF-8"))
    except websockets.exceptions.ConnectionClosed:
        await redis_pool.execute_pubsub("unsubscribe", channel)


def start_server(config):
    global redis_connection_host, redis_connection_db
    redis_connection_host = (config.redis_config.get("host"), config.redis_config.get("port"))
    redis_connection_db = config.redis_config.get("db")

    def thread_target():
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(websockets.serve(socket_handler, '', 5001))
        asyncio.get_event_loop().run_forever()

    threading.Thread(target=thread_target).start()

    def send_socket_message(message):
        print("Socket message 2: " + str(message))

    pubsub = storage.redis_instance.pubsub()
    pubsub.subscribe(**{'websocket': send_socket_message})


def generate_auth_token():
    token = str(uuid.uuid4()).replace("-", "")
    storage.redis_instance.setex(f"ws:auth:{token}", 30, "valid")
    return token


class ModuleWebsocket():
    def __init__(self, module_id):
        self.module_id = module_id

    def publish(self, key, data):
        storage.redis_instance.publish("websocket", json.dumps({
            "module_id": self.module_id,
            "key": key,
            "data": data
        }))
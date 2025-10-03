import asyncio
import json
from asyncio_mqtt import Client, MqttError
from db import save_telemetry

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
TOPIC = "smartcity/+/telemetry"

class Broadcaster:
    def __init__(self):
        self._clients = set()
    async def publish(self, msg):
        dead = []
        for ws in list(self._clients):
            try:
                await ws.send_json(msg)
            except Exception:
                dead.append(ws)
        for d in dead:
            self._clients.discard(d)
    async def connect(self, ws):
        self._clients.add(ws)
    def disconnect(self, ws):
        self._clients.discard(ws)

broadcaster = Broadcaster()

async def run_mqtt():
    reconnect_interval = 5
    while True:
        try:
            async with Client(MQTT_BROKER, port=MQTT_PORT) as client:
                async with client.unfiltered_messages() as messages:
                    await client.subscribe(TOPIC)
                    async for message in messages:
                        try:
                            payload = message.payload.decode()
                            data = json.loads(payload)
                            # guardar en DB
                            save_telemetry(data)
                            # notificar websocket clients
                            await broadcaster.publish(data)
                        except Exception as e:
                            print("Error procesando mensaje MQTT:", e)
        except MqttError as me:
            print("MQTT error:", me)
            await asyncio.sleep(reconnect_interval)

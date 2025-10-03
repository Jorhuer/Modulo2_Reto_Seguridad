import os
import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = os.environ.get("BROKER_HOST", "localhost")
PORT = int(os.environ.get("BROKER_PORT", 1883))
DEVICE_ID = os.environ.get("DEVICE_ID", "sim-001")
INTERVAL = int(os.environ.get("INTERVAL", 10))

TOPIC = f"smartcity/{DEVICE_ID}/telemetry"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker, rc=", rc)

def main():
    client = mqtt.Client(client_id=f"sim-{random.randint(0,9999)}")
    client.on_connect = on_connect
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        while True:
            payload = {
                "device_id": DEVICE_ID,
                "ts": int(time.time()),
                "temp": round(20 + random.random()*10, 2),
                "lat": 19.432608,
                "lon": -99.133209
            }
            msg = json.dumps(payload)
            print("Publishing:", msg)
            client.publish(TOPIC, msg)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

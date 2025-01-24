import paho.mqtt.client as mqtt
import time

from my_secrets import (
    CAMERA_READ_ENDPOINT,
    CLIENT_READ_ENDPOINT,
    PORT,
    HIVEMQ_HOST,
    HIVEMQ_PASSWORD,
    HIVEMQ_USERNAME,
)

import logging

logging.basicConfig(level=logging.DEBUG)


# Publish a command
def send_command(command):
    client.publish(CAMERA_READ_ENDPOINT, command)
    print(f"Sent command: {command}")


def receive_message(client, userdata, msg):
    received_message = msg.payload.decode("utf-8")
    print(f"Received message: {received_message}")


logger = logging.getLogger(__name__)

client = mqtt.Client()
client.enable_logger(logger)

client.on_message = receive_message

client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(HIVEMQ_USERNAME, HIVEMQ_PASSWORD)
client.connect(HIVEMQ_HOST, PORT)
client.subscribe(CLIENT_READ_ENDPOINT, qos=2)

send_command("capture")

client.loop_forever()

import os
import socket


class Config:
    ENCODING = 'utf-8'
    INTERVAL = 2  # in sec

    # ip address for local development
    HOST_IP = socket.gethostbyname(socket.gethostname())
    KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', f'{HOST_IP}:9092')

    KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'topic_1')

    # directory to put keys
    KEYS_DIRECTORY = os.environ.get('KEYS_DIRECTORY')

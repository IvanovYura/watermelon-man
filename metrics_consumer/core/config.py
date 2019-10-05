import os
import socket


class Config:
    ENCODING = 'utf-8'

    # ip address for local development
    HOST_IP = socket.gethostbyname(socket.gethostname())
    KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', f'{HOST_IP}:9092')

    KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'topic_1')

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 54320))
    DB_NAME = os.environ.get('DB_NAME', 'topic_1')
    DB_USER = os.environ.get('DB_USER', 'topic_1')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'topic_1')

    METRICS_BATCH_SIZE = os.environ.get('METRICS_BATCH_SIZE', 10)

    KEYS_DIRECTORY = os.environ.get('KEYS_DIRECTORY')

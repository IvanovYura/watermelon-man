import json

from kafka import KafkaConsumer
from core.config import Config
from core.consumer_utils import write_metrics_to_db
from core.db.database import db
from core.db.queries import create_table
from core.logger import logger

keys_directory = Config.KEYS_DIRECTORY

if not keys_directory:
    raise RuntimeError('Directory for SSL keys is not specified by KEYS_DIRECTORY')

consumer = KafkaConsumer(
    Config.KAFKA_TOPIC,
    bootstrap_servers=Config.KAFKA_BROKER_URL,
    value_deserializer=lambda value: json.loads(value.decode(Config.ENCODING)),
    security_protocol='SSL',
    ssl_cafile=f'{keys_directory}/ca.pem',
    ssl_certfile=f'{keys_directory}/service.cert',
    ssl_keyfile=f'{keys_directory}/service.key',
)

if __name__ == '__main__':
    try:
        connection = db.connect_with(
            Config.DB_HOST,
            Config.DB_PORT,
            Config.DB_NAME,
            Config.DB_USER,
            Config.DB_PASSWORD,
        )

        create_table(connection)

        write_metrics_to_db(connection, consumer)

    except KeyboardInterrupt:
        logger.info('\nExit') & exit(0)

    finally:
        db.close_connection()

import json

from kafka import KafkaConsumer
from psycopg2.extensions import connection

from core.config import Config
from core.consumer_utils import write_metrics_to_db
from core.db.database import db
from core.db.queries import create_table
from core.logger import logger


class Consumer:
    def __init__(self):
        self.consumer = self._init_kafka_consumer()

    @staticmethod
    def _init_kafka_consumer() -> KafkaConsumer:
        keys = Config.KEYS_DIRECTORY

        if not keys:
            raise RuntimeError('Directory for SSL keys is not specified by KEYS_DIRECTORY')

        return KafkaConsumer(
            Config.KAFKA_TOPIC,
            bootstrap_servers=Config.KAFKA_BROKER_URL,
            value_deserializer=lambda value: json.loads(value.decode(Config.ENCODING)),
            security_protocol='SSL',
            ssl_cafile=f'{keys}/ca.pem',
            ssl_certfile=f'{keys}/service.cert',
            ssl_keyfile=f'{keys}/service.key',
        )

    def write_metrics_to_db(self, conn: connection):
        write_metrics_to_db(conn, self.consumer)

    def close(self):
        if self.consumer:
            self.consumer.close()


def run():
    consumer = Consumer()

    try:
        connection = db.connect_with(
            Config.DB_HOST,
            Config.DB_PORT,
            Config.DB_NAME,
            Config.DB_USER,
            Config.DB_PASSWORD,
        )

        create_table(connection)

        consumer.write_metrics_to_db(connection)

    except KeyboardInterrupt:
        logger.info('\nExit') & exit(0)

    finally:
        db.close_connection()
        consumer.close()


if __name__ == '__main__':
    run()

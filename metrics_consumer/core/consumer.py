import json

from kafka import KafkaConsumer
from datetime import datetime
from core.config import Config
from core.db.database import db
from core.db.queries import insert_metrics
from core.logger import logger

consumer = KafkaConsumer(
    Config.KAFKA_TOPIC,
    bootstrap_servers=Config.KAFKA_BROKER_URL,
    value_deserializer=lambda value: json.loads(value.decode(Config.ENCODING)),
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
        metrics = []
        counter = 0
        inserted = False
        for message in consumer:

            message = message.value
            message['timestamp'] = datetime.fromtimestamp(message['timestamp'])
            message['metrics'] = json.dumps(message['metrics'])

            logger.info(f'Get message: {message}')

            if counter < Config.METRICS_BATCH_SIZE:
                metrics.append(message)
                counter += 1
                break

            insert_metrics(connection, metrics)
            inserted = True
            counter = 0

        if metrics and not inserted:
            insert_metrics(connection, metrics)

    except KeyboardInterrupt:
        logger.info('\nExit') & exit(0)

    finally:
        db.close_connection()

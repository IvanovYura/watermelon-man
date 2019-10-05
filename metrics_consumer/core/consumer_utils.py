import json

from jsonschema import ValidationError
from jsonschema.validators import validator_for
from kafka import KafkaConsumer
from datetime import datetime
from psycopg2.extensions import connection

from core.config import Config
from core.db.queries import insert_metrics
from core.logger import logger

SCHEMA = {
    'type': 'object',
    'properties': {
        'timestamp': {'type': 'number'},
        'metrics': {
            'type': 'object',
            'properties': {
                'cpu': {'type': 'number'},
            },
            'additionalProperties': True,
            'required': ['cpu'],
        },
    },
    'required': ['timestamp', 'metrics'],
    'additionalProperties': False,
}

VALIDATOR = validator_for(SCHEMA)(SCHEMA)


def _validate_message(message):
    try:
        VALIDATOR.validate(message)
    except ValidationError as e:
        raise RuntimeError(e)


def write_metrics_to_db(conn: connection, consumer: KafkaConsumer):
    """
    Writes metrics to database by batch
    """
    metrics = []
    counter = 0

    for message in consumer:

        message = message.value

        _validate_message(message)

        message['timestamp'] = datetime.fromtimestamp(message['timestamp'])
        message['metrics'] = json.dumps(message['metrics'])

        logger.info(f'Get message: {message}')

        # metrics mill be added to DB based on specified batch size, 10 by default
        if counter < Config.METRICS_BATCH_SIZE:
            metrics.append(message)
            counter += 1
            continue

        insert_metrics(conn, metrics)
        metrics.clear()
        counter = 0

    if metrics:
        insert_metrics(conn, metrics)

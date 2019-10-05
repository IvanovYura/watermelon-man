import json
from argparse import ArgumentParser
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from core.config import Config
from core.generator import MetricsGenerator
from core.logger import logger

ap = ArgumentParser(description='Generates specified OS metrics to be ingest by Kafka Provider')

ap.add_argument('--disk', required=False, action='append', help='disk usage metrics to collect')
ap.add_argument('--disk-path', required=False, help='disk path from where to collect disk usage statistics')
ap.add_argument('--memory', required=False, action='append', help='memory metrics to collect')
ap.add_argument('--interval', required=False, help='metrics gathering interval. 2 seconds is not specified')


def _get_kafka_producer() -> KafkaProducer:
    """
    Initialize Kafka Producer with specified Broker Url.

    If Consumer is not subscribed to the event bus, NoBrokersAvailable exception is raised:
    see kafka-console-consumer.sh for additional details.
    """
    try:
        return KafkaProducer(
            bootstrap_servers=Config.KAFKA_BROKER_URL,
            value_serializer=lambda value: json.dumps(value).encode(Config.ENCODING),
        )
    except NoBrokersAvailable:
        logger.error('Kafka subscriber/consumer was not set up') & exit(42)


def send_message(producer: KafkaProducer, message: dict):
    """
    Sends message to Kafka Topic
    """
    logger.info(f'Sending the message: {message}')

    producer.send(Config.KAFKA_TOPIC, value=message)


def generate_message(args: dict = None) -> dict:
    """
    Generates message based on arguments as metrics to collect
    """
    args = args if args else {}

    disk_metrics = args.get('disk') or []
    disk_path = args.get('disk_path')
    memory_metrics = args.get('memory') or []
    interval = args.get('interval')

    generator = MetricsGenerator(interval)

    generator.disk_usage_metrics_to_collect(*disk_metrics, path=disk_path)
    generator.memory_metrics_to_collect(*memory_metrics)

    return generator.create_message()


if __name__ == '__main__':
    args = vars(ap.parse_args())

    if not args.get('help'):
        producer = _get_kafka_producer()

        while True:
            try:
                message = generate_message(args)
                send_message(producer, message)
            except KeyboardInterrupt:
                logger.info('\nExit') & exit(0)

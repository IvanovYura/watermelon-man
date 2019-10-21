import json
from argparse import ArgumentParser

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from logger import logger
from config import Config
from publisher.producer_utils import generate_message

ap = ArgumentParser(description='Generates specified OS metrics to be ingest by Kafka Provider')

ap.add_argument('--disk', required=False, action='append', help='disk usage metrics to collect')
ap.add_argument('--disk-path', required=False, help='disk path from where to collect disk usage statistics')
ap.add_argument('--memory', required=False, action='append', help='memory metrics to collect')


class Producer:
    def __init__(self):
        self.producer = None  # self._init_kafka_producer()

    @staticmethod
    def _init_kafka_producer() -> KafkaProducer:
        """
        Initialize Kafka Producer with specified Broker Url.

        If Consumer is not subscribed to the event bus, NoBrokersAvailable exception is raised.
        """
        try:
            return KafkaProducer(
                bootstrap_servers=Config.KAFKA_BROKER_URL,
                value_serializer=lambda value: json.dumps(value).encode(Config.ENCODING)
            )

        except NoBrokersAvailable:
            logger.error('Kafka subscriber/consumer was not set up')
            raise

    def send_message(self, message: dict):
        """
        Sends message to Kafka Topic
        """
        logger.info(f'Sending the message: {message}')

        # self.publisher.send(Config.KAFKA_TOPIC, value=message)

    def close(self):
        if self.producer:
            self.producer.close()


def main():
    args = vars(ap.parse_args())

    if not args.get('help'):
        producer = Producer()

        try:
            while True:
                message = generate_message(args)
                producer.send_message(message)

        except KeyboardInterrupt:
            logger.info('\nExit')
            exit(1)

        finally:
            producer.close()


if __name__ == '__main__':
    main()

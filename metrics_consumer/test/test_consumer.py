import json
from datetime import datetime
from unittest import TestCase, mock
from unittest.mock import MagicMock

from core.config import Config
from core.consumer import Consumer
from core.db.queries import SQL_INSERT_METRICS


class ConsumerTest(TestCase):

    def setUp(self):
        Config.KEYS_DIRECTORY = '../keys'

    @mock.patch('core.consumer.KafkaConsumer')
    def test__init_consumer(self, consumer_mock):
        consumer = Consumer()

        args_list = consumer_mock.call_args_list
        args = args_list[0][1]
        self.assertEqual(args['bootstrap_servers'], Config.KAFKA_BROKER_URL)
        # check arguments
        self.assertIn('value_deserializer', args)
        self.assertIn('security_protocol', args)
        self.assertIn('ssl_cafile', args)
        self.assertIn('ssl_certfile', args)
        self.assertIn('ssl_keyfile', args)

    def test__init_consumer_keys_are_not_provided(self):
        Config.KEYS_DIRECTORY = None

        with self.assertRaises(RuntimeError) as e:
            consumer = Consumer()

        self.assertEqual(str(e.exception), 'Directory for SSL keys is not specified by KEYS_DIRECTORY')

    @mock.patch('core.db.queries.extras')
    @mock.patch('core.consumer.KafkaConsumer')
    @mock.patch('core.consumer.db')
    def test__write_metrics_to_db_one_message(self, db_mock, consumer_mock, extras_mock):
        dt = datetime(2019, 10, 4)
        message = {
            'timestamp': dt.timestamp(),
            'metrics': {
                'cpu': 1,
                'disk': {
                    'free': 2,
                    'percent': 3.0,
                },
                'memory': {
                    'available': 4,
                },
            }
        }
        consumer_mock.return_value = [MagicMock(value=message)]

        consumer = Consumer()
        consumer.write_metrics_to_db(db_mock)

        args = extras_mock.execute_batch.call_args_list[0][0]

        self.assertEqual(args[1], SQL_INSERT_METRICS)
        self.assertEqual(args[2], [{
            'metrics': json.dumps(message['metrics']),
            'timestamp': dt,
        }])

    @mock.patch('core.db.queries.extras')
    @mock.patch('core.consumer.KafkaConsumer')
    @mock.patch('core.consumer.db')
    def test__write_metrics_to_db_batch_size_messages(self, db_mock, consumer_mock, extras_mock):
        dt = datetime(2019, 10, 4)
        message = {
            'timestamp': dt.timestamp(),
            'metrics': {
                'cpu': 1,
                'disk': {
                    'free': 2,
                    'percent': 3.0,
                },
                'memory': {
                    'available': 4,
                },
            }
        }
        consumer_mock.return_value = [MagicMock(value=message)] * Config.METRICS_BATCH_SIZE

        consumer = Consumer()
        consumer.write_metrics_to_db(db_mock)

        args = extras_mock.execute_batch.call_args_list[0][0]

        self.assertEqual(args[1], SQL_INSERT_METRICS)
        self.assertEqual(args[2], [
            {
                'metrics': json.dumps(message['metrics']),
                'timestamp': dt,
            }
            for message in [message] * Config.METRICS_BATCH_SIZE])

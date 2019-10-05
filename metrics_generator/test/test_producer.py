from unittest import TestCase, mock
from datetime import datetime

from kafka.errors import NoBrokersAvailable

from core.config import Config
from core.producer import generate_message, _get_kafka_producer, send_message


class ProducerTest(TestCase):

    @mock.patch('core.producer.KafkaProducer')
    def test__init_producer(self, kafka_producer_mock):
        _get_kafka_producer()

        args_list = kafka_producer_mock.call_args_list
        args = args_list[0][1]
        self.assertEqual(args['bootstrap_servers'], Config.KAFKA_BROKER_URL)
        # check arguments
        self.assertIn('value_serializer', args)
        self.assertIn('security_protocol', args)
        self.assertIn('ssl_cafile', args)
        self.assertIn('ssl_certfile', args)
        self.assertIn('ssl_keyfile', args)
        self.assertIn('api_version', args)

    @mock.patch('core.producer.logger')
    @mock.patch('core.producer.KafkaProducer', side_effect=NoBrokersAvailable)
    def test__init_producer_broker_not_specified_fail(self, kafka_producer_mock, logger_mock):
        # exit when no broker available
        with self.assertRaises(SystemExit) as cm:
            _get_kafka_producer()

        logger_mock.error.assert_called_with('Kafka subscriber/consumer was not set up')
        self.assertEqual(cm.exception.code, 42)

    @mock.patch('core.generator.datetime')
    @mock.patch('core.generator.cpu_percent')
    @mock.patch('core.generator.disk_usage')
    @mock.patch('core.generator.virtual_memory')
    @mock.patch('core.producer.KafkaProducer')
    def test__send_producer_with_message(
            self,
            kafka_producer_mock,
            virtual_memory_mock,
            dick_usage_mock,
            cpu_percent_mock,
            datetime_mock,
    ):
        send_method = kafka_producer_mock.return_value.send

        dt = datetime(2019, 10, 4)

        virtual_memory_mock.return_value.free = 20
        dick_usage_mock.return_value.used = 10
        cpu_percent_mock.return_value = 42
        datetime_mock.utcnow.return_value = dt

        args = {
            'disk': ['used'],
            'memory': ['free'],
        }

        msg = generate_message(args)

        producer = _get_kafka_producer()
        send_message(producer, msg)

        send_method.assert_called_with(Config.KAFKA_TOPIC, value=msg)

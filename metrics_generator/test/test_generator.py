from datetime import datetime
from unittest import TestCase, mock

from core.generator import MetricsGenerator


class MetricsGeneratorTest(TestCase):

    def setUp(self):
        self.metrics_generator = MetricsGenerator()

    @mock.patch('core.generator.datetime')
    @mock.patch('core.generator.cpu_percent')
    def test__message_created_with_cpu_by_default(self, cpu_percent_mock, datetime_mock):
        dt = datetime(2019, 10, 4)
        cpu_percent_mock.return_value = 42
        datetime_mock.utcnow.return_value = dt

        expected_message = {
            'timestamp': dt.timestamp(),
            'metrics': {'cpu': 42}
        }
        message = self.metrics_generator.create_message()

        self.assertEqual(message, expected_message)

    @mock.patch('core.generator.datetime')
    @mock.patch('core.generator.cpu_percent')
    @mock.patch('core.generator.disk_usage')
    @mock.patch('core.generator.virtual_memory')
    def test__message_created_with_specified_metrics(
            self,
            virtual_memory_mock,
            dick_usage_mock,
            cpu_percent_mock,
            datetime_mock
    ):
        dt = datetime(2019, 10, 4)

        virtual_memory_mock.return_value.free = 20
        dick_usage_mock.return_value.used = 10
        cpu_percent_mock.return_value = 42
        datetime_mock.utcnow.return_value = dt

        self.metrics_generator.disk_usage_metrics_to_collect('used')
        self.metrics_generator.memory_metrics_to_collect('free')

        expected_message = {
            'timestamp': dt.timestamp(),
            'metrics': {
                'cpu': 42,
                'disk': {'used': 10, 'path': '/'},
                'memory': {'free': 20},
            }
        }
        message = self.metrics_generator.create_message()

        self.assertEqual(message, expected_message)

    def test__collect_disk_metrics_one_success(self):
        self.metrics_generator.disk_usage_metrics_to_collect('used')
        self.assertEqual(self.metrics_generator._disk_usage_metrics, {'used'})
        # default path
        self.assertEqual(self.metrics_generator._path, '/')

    def test__collect_disk_metrics_one_failure(self):
        with self.assertRaises(ValueError) as e:
            self.metrics_generator.disk_usage_metrics_to_collect('use')
        self.assertEqual(str(e.exception), 'The type of disk usage metric is invalid: {\'use\'}')

    def test__collect_disk_metrics_multiple_success(self):
        self.metrics_generator.disk_usage_metrics_to_collect('used', 'percent')
        self.assertEqual(self.metrics_generator._disk_usage_metrics, {'used', 'percent'})
        # default path
        self.assertEqual(self.metrics_generator._path, '/')

    def test__collect_disk_metrics_custom_path(self):
        self.metrics_generator.disk_usage_metrics_to_collect(path='/new_path')
        self.assertEqual(self.metrics_generator._path, '/new_path')

    def test__collect_memory_metrics_one_success(self):
        self.metrics_generator.memory_metrics_to_collect('free')
        self.assertEqual(self.metrics_generator._memory_metrics, {'free'})

    def test__collect_memory_metrics_one_failure(self):
        with self.assertRaises(ValueError) as e:
            self.metrics_generator.memory_metrics_to_collect('use')
        self.assertEqual(str(e.exception), 'The type of memory metric is invalid: {\'use\'}')

    def test__collect_memory_metrics_multiple_success(self):
        self.metrics_generator.memory_metrics_to_collect('used', 'available')
        self.assertEqual(self.metrics_generator._memory_metrics, {'used', 'available'})

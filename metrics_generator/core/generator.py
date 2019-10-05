from datetime import datetime
from psutil import cpu_percent, virtual_memory, disk_usage

from core.config import Config

MEMORY_AVAILABLE_METRICS = {'used', 'available', 'free'}
DISK_USAGE_AVAILABLE_METRICS = {'used', 'free', 'percent'}

DEFAULT_PATH = '/'


class MetricsGenerator:
    """
    Represents an OS metrics generator/collector.

    Metrics are collected in the OS in specific interval,
    if interval is note specified, default 2 seconds is used.
    """

    def __init__(self, interval=None):
        self._memory_metrics = set()
        self._disk_usage_metrics = set()
        self._path = None

        if not interval:
            self._interval = Config.INTERVAL

    def create_message(self) -> dict:
        """
        Returns message contained generated metrics.

        CPU metric is set up by default,
        to specify which disk or memory metrics should be collected appropriate methods are used:
        disk_usage__metrics_to_collect() or memory_metrics_to_collect()
        """
        return {
            'timestamp': datetime.utcnow().timestamp(),
            'metrics': {
                'cpu': cpu_percent(self._interval),
                **self._get_disk_usage_metrics(),
                **self._get_memory_metrics(),
            }
        }

    def _get_memory_metrics(self) -> dict:
        """
        Returns memory metrics dictionary based on memory metrics to collect:
        see memory_metrics_to_collect() method.
        """
        memory_metrics = {
            metric: virtual_memory().__getattribute__(metric)
            for metric in self._memory_metrics
        }
        return {'memory': memory_metrics} if memory_metrics else {}

    def _get_disk_usage_metrics(self) -> dict:
        """
        Returns disk usage metrics dictionary based on disk metrics to collect:
        see disk_usage__metrics_to_collect() method.
        """
        disk_usage_metrics = {
            metric: disk_usage(self._path).__getattribute__(metric)
            for metric in self._disk_usage_metrics
        }
        if not disk_usage_metrics:
            return {}

        disk_usage_metrics.update({
            'path': self._path,
        })
        return {'disk': disk_usage_metrics}

    def memory_metrics_to_collect(self, *args):
        """
        Specified which memory metrics to collect:

        - used:
            memory used in bytes

        - available:
            the memory in bytes that can be given instantly to processes without the
            system going into swap

        - free:
            not used memory in bytes

        """
        diff = set(args) - MEMORY_AVAILABLE_METRICS
        if diff:
            raise ValueError(f'The type of memory metric is invalid: {diff}')
        self._memory_metrics.update(args)

    def disk_usage_metrics_to_collect(self, *args, path: str = None):
        """
        Specified which disk usage metrics to collect in specified path:

        - used:
            used memory in bytes in specified path

        - free:
            free memory in bytes

        - percent:
            used memory in percent

        If path is not specified, default root directory is used.
        """
        self._path = path if path else DEFAULT_PATH

        diff = set(args) - DISK_USAGE_AVAILABLE_METRICS
        if diff:
            raise ValueError(f'The type of disk usage metric is invalid: {diff}')
        self._disk_usage_metrics.update(args)

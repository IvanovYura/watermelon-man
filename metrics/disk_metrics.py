from psutil import disk_usage

from metrics.base import BaseMetrics


class DiskMetrics(BaseMetrics):
    AVAILABLE_METRICS = {'used', 'free', 'percent'}

    DEFAULT_PATH = '/'

    @classmethod
    def collect(cls, *args, **kwargs) -> dict:
        """
        Returns disk usage metrics dictionary.
        """
        cls.validate(args)

        path = kwargs.get('path') or cls.DEFAULT_PATH

        disk_usage_metrics = {
            metric: getattr(disk_usage(path), metric)
            for metric in args
        }
        if not disk_usage_metrics:
            return {}

        disk_usage_metrics.update({
            'path': path,
        })
        return {'disk': disk_usage_metrics}

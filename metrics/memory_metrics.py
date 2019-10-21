from psutil import virtual_memory

from metrics.base import BaseMetrics


class MemoryMetrics(BaseMetrics):
    AVAILABLE_METRICS = {'used', 'available', 'free'}

    @classmethod
    def collect(cls, *args) -> dict:
        """
        Returns memory metrics dictionary.
        """
        if args:
            cls.validate(args)

        memory_metrics = {
            metric: getattr(virtual_memory(), metric)
            for metric in args
        }
        return {'memory': memory_metrics} if memory_metrics else {}

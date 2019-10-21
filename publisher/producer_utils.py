from datetime import datetime

from metrics.disk_metrics import DiskMetrics
from metrics.memory_metrics import MemoryMetrics


def generate_message(args: dict = None) -> dict:
    """
    Generates message based on arguments passed in CLI.

    Raises ValueError if argument is not supported.
    """
    args = args if args else {}

    disk_metrics = args.get('disk') or []
    disk_path = args.get('disk_path')
    memory_metrics = args.get('memory') or []

    return {
        'timestamp': datetime.utcnow().timestamp(),
        'metrics': {
            # TODO: add CPU metric
            **DiskMetrics.collect(*disk_metrics, path=disk_path),
            **MemoryMetrics.collect(*memory_metrics),
        }
    }

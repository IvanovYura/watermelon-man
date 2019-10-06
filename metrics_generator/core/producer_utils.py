from core.generator import MetricsGenerator


def generate_message(args: dict = None) -> dict:
    """
    Generates message based on arguments as metrics to collect.

    Raises ValueError if argument is not supported.
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

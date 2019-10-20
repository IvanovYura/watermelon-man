class BaseMetrics:
    AVAILABLE_METRICS: set

    @classmethod
    def collect(cls) -> dict:
        """
        Implements the collects metric logic.
        Result should be serializable JSON.
        """
        raise NotImplementedError

    @classmethod
    def validate(cls, *args):
        diff = set(args) - cls.AVAILABLE_METRICS

        if diff:
            raise ValueError(f'The provided metrics is invalid: {diff}')

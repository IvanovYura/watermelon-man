from logging import Logger, getLogger, StreamHandler, INFO, Formatter
import sys

LOG_FORMAT_SHORT = "%(levelname)s\t%(message)s"


def init_logger(level: int, handler: StreamHandler) -> Logger:
    """
    Returns logger with output to STDOUT
    """
    logger = getLogger()
    logger.setLevel(level)

    logger.addHandler(handler)
    formatter = Formatter(LOG_FORMAT_SHORT)
    handler.setFormatter(formatter)

    return logger


logger = init_logger(INFO, StreamHandler(sys.stdout))

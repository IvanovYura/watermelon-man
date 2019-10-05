from logging import Logger, getLogger, StreamHandler, INFO
import sys


def init_logger(level: int) -> Logger:
    """
    Returns logger with output to STDOUT
    """
    logger = getLogger()
    logger.setLevel(level)

    handler = StreamHandler(sys.stdout)
    logger.addHandler(handler)

    return logger


logger = init_logger(INFO)

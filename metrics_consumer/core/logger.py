import logging
import sys


def init_logger(level: int) -> logging.Logger:
    """
    Returns logger with output to STDOUT
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    return logger


logger = init_logger(logging.INFO)

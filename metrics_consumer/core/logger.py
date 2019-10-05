import logging
import sys


def init_logger(level: int, handler: logging.StreamHandler) -> logging.Logger:
    """
    Returns logger with output to STDOUT
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    logger.addHandler(handler)

    return logger


logger = init_logger(logging.INFO, logging.StreamHandler(sys.stdout))

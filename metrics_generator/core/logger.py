from logging import Logger, getLogger, StreamHandler, INFO
import sys


def init_logger(level: int, handler: StreamHandler) -> Logger:
    """
    Returns logger with output to STDOUT
    """
    logger = getLogger()
    logger.setLevel(level)

    logger.addHandler(handler)

    return logger


logger = init_logger(INFO, StreamHandler(sys.stdout))

import logging
from utils.logger import Logger


def test_logger_returns_logger_instance():
    logger = Logger("test").get_logger()
    assert isinstance(logger, logging.Logger)
    logger.info("Test info log")
    logger.warning("Test warning log")
    logger.error("Test error log")
    # No exception should be raised, and logger should be reusable


def test_logger_singleton():
    logger1 = Logger("test").get_logger()
    logger2 = Logger("test").get_logger()
    assert logger1 is logger2

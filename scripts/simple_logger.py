import logging


def create_logger():
    """Simple logger for debug"""
    log_format = '%(asctime)s %(message)s'
    logging.basicConfig(format=log_format)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.info(__file__)
    return logger


logger = create_logger()

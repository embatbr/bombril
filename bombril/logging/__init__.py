#! coding: utf-8

import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
)


def get_logger(name, level_name='INFO'):
    logger = logging.getLogger(name)
    level = getattr(logging, level_name, logging.NOTSET)
    logger.setLevel(level)

    return logger

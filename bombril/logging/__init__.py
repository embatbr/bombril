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

    # TODO remove the duplication

    def log_critical(self):
        func = self.critical
        def _internal(msg, *args):
            func(msg.format(*args))
        return _internal

    logger.critical = log_critical

    def log_error(self):
        func = self.error
        def _internal(msg, *args):
            func(msg.format(*args))
        return _internal

    logger.error = log_error(logger)

    def log_warning(self):
        func = self.warning
        def _internal(msg, *args):
            func(msg.format(*args))
        return _internal

    logger.warning = log_warning(logger)

    def log_info(self):
        func = self.info
        def _internal(msg, *args):
            func(msg.format(*args))
        return _internal

    logger.info = log_info(logger)

    def log_debug(self):
        func = self.debug
        def _internal(msg, *args):
            func(msg.format(*args))
        return _internal

    logger.debug = log_debug(logger)

    return logger

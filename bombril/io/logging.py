#! coding: utf-8

"""Deals with logging (read and write logs, manage log files and etc.).
"""


import logging


def get_logger(name, level=None):
    logger = logging.getLogger(name)
    logger.setLevel(level or logging.INFO)
    return logger

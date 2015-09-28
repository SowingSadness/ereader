# -*- coding: utf-8 -*-
import os
import logging
import logging.config
from importlib import import_module

from .logging_config import DEFAULT_LOGGING_CONFIG
from .exceptions import ConfigureError


DEV_BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.path.pardir
    )
)


def get_logger(name, verbosity=None):
    """ хелпер для получения логгера """

    logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
    logger = logging.getLogger(name)

    if verbosity is not None:
        logger.setLevel({
            0: logging.NOTSET,
            1: logging.ERROR,
            2: logging.INFO,
            3: logging.DEBUG,
            '0': logging.NOTSET,
            '1': logging.ERROR,
            '2': logging.INFO,
            '3': logging.DEBUG
        }.get(verbosity, logging.NOTSET))

    return logger


def load_class(path):
    """ хелпер для загрузки классов """

    try:
        mod_name, cls_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except AttributeError as e:
        raise ConfigureError('Error importing {0}: "{1}"'.format(mod_name, e))

    try:
        cls = getattr(mod, cls_name)
    except AttributeError:
        raise ConfigureError(
            'Module "{0}" does not define a "{1}" class'.format(
                mod_name, cls_name))

    return cls


def abs_path(path, base_dir=DEV_BASE_DIR):
    if path.startswith('.'):
        path = os.path.abspath(os.path.join(base_dir, path))
    return path


def ensure_dir(path):
    path = abs_path(path)
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError as e:
            raise ConfigureError("Can't make dir. Error: {0}".format(e))
    return path

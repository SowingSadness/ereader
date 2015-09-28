#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
#from optparse import OptionParser, make_option
from argparse import ArgumentParser
from ConfigParser import ConfigParser

from .main import EReaderApplication
from .exceptions import ConfigureError
from .utils import get_logger


VERBOSITY_CHOICES = ['0', '1', '2', '3']
DEFAULT_CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'ereader.ini'))


def main():
    parser = ArgumentParser(description='Effective Reader')
    parser.add_argument(
        '-c', '--config', help="Reader config file",
        default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        'urls', metavar='URL', type=str, nargs='+',
        help="Urls for read")
    parser.add_argument(
        '-v', '--verbosity', choices=VERBOSITY_CHOICES,
        help="Verbose level", default=None)
    parser.add_argument(
        '-s', '--short', action='store_true',
        help="Short view")

    args = parser.parse_args()
    log = get_logger('ereader', args.verbosity)

    if not os.path.isfile(args.config):
        log.error("Config file not found")
        sys.exist(1)

    config = ConfigParser()
    readed = config.read([os.path.expanduser('~/.ereader.ini'), args.config])
    log.debug('Read configs: %s', ', '.join(readed))

    if args.verbosity is not None:
        config.set('main', 'verbosity', str(args.verbosity))
    if args.short is not None:
        config.set('main', 'short', str(args.short))

    app = EReaderApplication(config)

    try:
        app.configure(args.config)
        app.run(args.urls)
    except AssertionError as e:
        log.warning(e)
    except ConfigureError as e:
        log.error('Configure error: %s', e)
        sys.exit(1)

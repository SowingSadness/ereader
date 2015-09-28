# -*- coding: utf-8 -*-
from urlparse import urlparse

from .utils import get_logger
from .exceptions import ConfigureError

from .documents.dumper import DumpersManager
from .readers import ReadersManager
from .documents import HtmlDocument, TextDocument


class EReaderApplication(object):
    def __init__(self, config):
        self.config = config
        self.log = get_logger(
            __name__, verbosity=config.getint('main', 'verbosity'))

    def configure(self, config_file):

        self.log.debug("Configure application {0}".format(
            self.__class__.__name__))

        if not self.config.has_option('main', 'readers'):
            raise ConfigureError(
                "Improperly configuration. Can't find readers")

        # configure readers
        self.readers_manager = ReadersManager(
            logger_verbosity=self.config.getint('main', 'verbosity'))
        self.readers_manager.load_plugins(
            self.config.get('main', 'readers').split())
        self.readers_manager.configure_plugins(self.config)

        # configure dumpers
        self.dumpers_manager = DumpersManager(
            logger_verbosity=self.config.getint('main', 'verbosity'))
        self.dumpers_manager.load_plugins(
            self.config.get('main', 'dumpers').split())
        self.dumpers_manager.configure_plugins(self.config)

    def run(self, urls):
        self.log.debug("Run")

        for url_raw in urls:
            url = urlparse(url_raw)

            reader = self.readers_manager.choice_reader_by_scheme(url.scheme)
            if reader is None:
                continue

            content = reader.read(url)
            if content is None:
                continue

            html_document = HtmlDocument(content, 'utf-8')
            text_document = TextDocument(html_document.get_document_title())
            text_document.add_title(html_document.get_title())
            map(text_document.add_paragraph, html_document.get_paragraphs())

            for name, dumper in self.dumpers_manager.plugins:
                ctx = {'url': url,
                       'short': self.config.getboolean('main', 'short')}
                dumper.dump(text_document, **ctx)

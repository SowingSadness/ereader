import sys
import codecs

from ..plugin import BasePlugin, BasePluginManager
from ..exceptions import ConfigureError

import utils

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib2 import urlopen, HTTPError


class ReadersManager(BasePluginManager):
    def choice_reader_by_scheme(self, scheme):
        if not self.plugins:
            raise ConfigureError("section `readers` not found")

        for name, reader in self.plugins:
            if reader.is_support(scheme):
                return reader
        return self.log.error(
            "Can't do choice the reader for scheme `%s`", scheme)


class CommonReader(BasePlugin):
    # supported schemes for read
    schemes = ('file', 'http')

    def is_support(self, scheme):
        return scheme in self.schemes

    def _ensure_encoding(self, content, encoding):
        self.log.debug('Detected {0} encoding'.format(encoding))
        return content.decode(encoding, 'replace')

    def read(self, url):
        content = None
        self.log.info("Open: {0}".format(url.geturl()))
        if url.scheme.lower() == 'http':
            try:
                content = urlopen(url.geturl()).read()
            except (IOError, HTTPError):
                return self.log.error("Cant open url %s", url.geturl())
            self.log.debug('Open url: {0}'.format(url.path))
        elif url.scheme.lower() == 'file':
            with codecs.open(url.path, 'r') as html_file:
                content = html_file.read()
        else:
            return self.log.error("Can't open scheme: %s", url.scheme)

        encoding = utils.detect_encoding(content, self.config['encoding'])
        content = self._ensure_encoding(content, encoding)

        return content

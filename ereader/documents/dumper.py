from __future__ import print_function

import os
import sys
import platform
import codecs

from ..plugin import BasePlugin, BasePluginManager
from ..utils import ensure_dir, abs_path

try:
    import colorama
except ImportError:
    colorama = None


class DumpersManager(BasePluginManager):
    pass


class StdoutDumper(BasePlugin):
    def dump(self, document, **context):
        print(document, file=sys.stdout)
        self.log.debug('Document dumped to stdout')


class ConsoleDumper(StdoutDumper):
    def get_stream(self):
        if platform.system().lower() == 'windows':
            colorama.init(wrap=False, autoreset=True)
            stream = colorama.AnsiToWin32(sys.stderr).stream
        else:
            colorama.init(autoreset=True)
            stream = sys.stdout
        return stream

    @staticmethod
    def colored_title(text, settings):
        return colorama.Fore.RED + text

    @staticmethod
    def colored_paragraph(text, settings):
        return colorama.Fore.GREEN + text

    def dump(self, document, **context):
        if colorama is None:
            return super(ConsoleDumper, self).dump(document)

        document.formatters.add(
            document.formatters.TITLE, self.colored_title)
        document.formatters.add(
            document.formatters.PARAGRAPH, self.colored_paragraph)

        print(unicode(document.view(context['short'])), file=self.get_stream())


class FileDumper(BasePlugin):
    def get_out_filename(self, url):
        out_name = os.path.basename(url.path)
        out_ext = self.config.get('out_ext')

        if not out_name and not out_name.endswith('html'):
            out_name = '{0}.{1}'.format(url.netloc, out_ext)

        if not out_name.endswith(out_ext):
            name, _ = os.path.splitext(out_name)
            out_name = '{0}.{1}'.format(name, out_ext)

        out_file_name = self.config.get('file_name').format(
            base_dir=abs_path(self.config['dump_dir']),
            cur_dir=abs_path(self.config['dump_dir'], base_dir=os.getcwd()),
            domain=url.netloc,
            path=os.path.dirname(url.path),
            document_name=out_name
        )

        return out_file_name

    def dump(self, document, **context):
        assert 'url' in context, "context['url'] should be set"

        file_path = self.get_out_filename(context['url'])
        ensure_dir(os.path.dirname(file_path))

        with codecs.open(file_path, "w+", self.config['out_encoding']) as f:
            print(unicode(document.view(context['short'])), file=f)
        self.log.debug("Dump to {0}".format(file_path))

import os
import sys
import pytest
import glob
from urlparse import urlparse
from ConfigParser import ConfigParser

# FIXME after build release
PACKAGE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir))
sys.path.insert(0, PACKAGE_PATH)

from ereader.main import EReaderApplication
from ereader.readers import CommonReader
from ereader.readers.document import HtmlDocument

CONFIG = os.path.join(PACKAGE_PATH, 'ereader.ini')
URLS_LIST_PATH = os.path.join(os.path.dirname(__file__), 'urls.txt')
STATIC_SAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'static')


@pytest.fixture(scope="module")
def reader():
    config = ConfigParser()
    config.read([CONFIG, ])

    reader = CommonReader()
    reader.set_logger('ereader', 3)
    reader.config = dict(config.items('readers.CommonReader'))

    return reader


def get_example_url(lang, num):
    test_file = glob.glob(
        os.path.join(STATIC_SAMPLES_DIR, lang, '{0}*'.format(num)))
    if not test_file or not os.path.isfile(test_file[0]):
        raise OSError("File not found")

    example_url = 'file://{0}'.format(test_file[0])

    return example_url


class TestHtmlDocument(object):
    def test_ru(self, reader):
        for num in (1, 2):
            url = urlparse(get_example_url('ru', num))
            document = reader.create_document(url)
            document.get_title()

    def test_en(self, reader):
        pass

import re
from chardet import detect
#from textwrap import TextWrapper, _unicode
from xml.etree import ElementTree
from uuid import uuid4

from HTMLParser import HTMLParser


ENTITIES = {
    u'\u2014': '-',
    u'\u2013': '-',
    u'\u00A0': ' ',
    u'\u00AB': '"',
    u'\u00BB': '"',
    u'&mdash;': '-',
    u'&ndash;': '-',
    u'&quot;': '"',
}

WRONG_CHARSET = {
    'maccyrillic': 'cp1251',
    'win1251': 'cp1251',
    'win-1251': 'cp1251',
    'windows-1251': 'cp1251',
}

RE_CONTENT = re.compile(
    r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', re.I)
RE_CHARSET = re.compile(
    r'<meta.*?charset=["\']*(.+?)["\'>]', re.I)


def unescape_entities(text):
    if not text:
        return ""

    for entity, r in ENTITIES.items():
        if entity in text:
            text = text.replace(entity, r)

    return text


def strip_spaces(text):
    if not text:
        return ""
    return ' '.join(text.split())


def clean_tags(text):
    return re.sub(r'(\s*</?[^>]*>)+\s*', r' ', text).strip()


def detect_encoding(text, default='utf-8'):
    declarations = (RE_CONTENT.findall(text) + RE_CHARSET.findall(text))

    # detect encoding by declaration
    for enc in declarations:
        try:
            encoding = WRONG_CHARSET.get(enc.lower(), default)
            text.decode()

            return encoding
        except UnicodeDecodeError:
            pass

    return detect(clean_tags(text))['encoding'] or default


def truncate_text(text, limit=80):
    """ """

    try:
        limit = int(limit)
    except ValueError:
        return text

    if len(text) <= limit:
        return text

    text = text[:limit]
    words = text.split(' ')[:-1]

    return ' '.join(words) + '...'


def iterparent(tree):
    for parent in tree.getiterator():
        for child in parent:
            yield parent, child


def get_text_of(el, try_tags=('span', 'div')):
    out_el = None
    if el is None:
        return
    if el.text is not None and len(el.text) > 0:
        out_el = el
    else:
        assert isinstance(try_tags, tuple)
        for try_tag in try_tags:
            try_el = el.find('.//{0}'.format(try_tag))
            if try_el is None:
                continue
            if try_el.text is not None and len(try_el.text) > 0:
                out_el = try_el
                break
    if out_el is None:
        return
    return out_el.text


class SimpleHtmlParser(HTMLParser):
    def __init__(self):
        self.root = None
        self.tree = []
        HTMLParser.__init__(self)

    def feed(self, data):
        HTMLParser.feed(self, data)
        return self.root

    def handle_starttag(self, tag, attrs):
        if 'uuid' not in attrs:
            attrs.append(('uuid', str(uuid4())))

        if len(self.tree) == 0:
            element = ElementTree.Element(
                tag, dict(self.__filter_attrs(attrs)))
            self.tree.append(element)
            self.root = element
        else:
            element = ElementTree.SubElement(
                self.tree[-1], tag, dict(self.__filter_attrs(attrs)))
            self.tree.append(element)

    def handle_endtag(self, tag):
        self.tree.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)
        pass

    def handle_data(self, data):
        if self.tree:
            if (self.tree[-1].text is not None
                    and len(self.tree[-1].text) > 0):
                self.tree[-1].text += data
            else:
                self.tree[-1].text = data

    def get_root_element(self):
        return self.root

    def __filter_attrs(self, attrs):
        return filter(lambda x: x[0] and x[1], attrs) if attrs else []

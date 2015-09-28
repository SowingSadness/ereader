import re
from chardet import detect


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

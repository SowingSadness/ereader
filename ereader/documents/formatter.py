from __future__ import unicode_literals

import re
import os
from textwrap import wrap

RE_LINK_PATTERN = r'<a(?:.*)?>.*</a>'
RE_LINK_SUB_PATTERN = (
    r'<a(?:.*href=[\'"](?P<link>[^\'"]*)[\'"])?[^>]*>'
    r'(?P<title>((?!</?a>).)*)</a>'
)

RE_REPLACE_TMPLS = (
    r'[\g<title>|\g<link>]',
    r'[\g<link>]',
    r'[\g<title>]'
)

RE_WRAPPED_LINK = r'(\[[^\]\[]*\])+'


class FormatterManager(object):
    PARAGRAPH, TITLE = 'p', 't'

    def __init__(self):
        self._formatters = {
            self.PARAGRAPH: [
                paragraph_indent,
                link_transform,
                clean_tags,
                text_word_wrap,
            ],
            self.TITLE: [
                title_space,
                capitalize,
            ]
        }

    def add(self, to, formatter, order=None):
        assert to in (self.PARAGRAPH, self.TITLE)

        if order is None:
            order = len(self._formatters[to])
        self._formatters[to].insert(order, formatter)

    def iter_by(self, by):
        return iter(self._formatters[by])

    def __getitem__(self, key):
        return self._formatters[key]


# TODO add support link base url
def link_transform(text, settings):
    if not settings.get('links_transform'):
        return text

    lines = []
    for line in text.split(os.linesep):
        if not re.search(RE_LINK_PATTERN, line, re.I):
            lines.append(line)
            continue

        new_link_text = ''
        for tmpl in RE_REPLACE_TMPLS:
            try:
                new_link_text = re.sub(
                    RE_LINK_SUB_PATTERN, tmpl, line, flags=re.I)
            except re.error:
                continue
            else:
                break
        lines.append(new_link_text and new_link_text or line)

    if not lines:
        return text

    return os.linesep.join(lines)


def paragraph_indent(text, settings):
    if not settings.get('paragraph_indent_width'):
        return text
    return '{0}{1}'.format(
        ' ' * settings['paragraph_indent_width'],
        text
    )


def text_word_wrap(text, settings):
    if not settings.get('word_wrap_width'):
        return text

    if (settings.get('link_transform') and
            re.search(RE_WRAPPED_LINK, text)):
        list_links = re.findall(RE_WRAPPED_LINK, text)
        text = re.sub(RE_WRAPPED_LINK, '{}', text)

        lines = wrap(text, width=settings['word_wrap_width'])
        return os.linesep.join(lines).format(*list_links)

    return os.linesep.join(
        wrap(text, width=settings['word_wrap_width']))


def title_space(text, settings, size=1):
    return '{0}{1}'.format(
        text.rstrip(), os.linesep * size)

def clean_tags(text, settings):
    return re.sub(r'(\s*</?[^>]*>)+\s*', r' ', text).strip()


def capitalize(text, settings):
    if text is None:
        return text

    try:
        t1, t2 = text.split(' ', 1)
    except ValueError:
        return text
    return '{0} {1}'.format(t1.title(), t2)

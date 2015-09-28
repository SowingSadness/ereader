import os
import utils
import formatter

from xml.etree import ElementTree

from .stat import StatisticalMap
from .utils import iterparent, get_text_of


class BaseDocument(object):
    def __init__(self, *args, **kw):
        self.log = kw.get('logger')


class HtmlDocument(BaseDocument):
    def __init__(self, content, encoding, **kw):
        super(HtmlDocument, self).__init__(**kw)

        parser = utils.SimpleHtmlParser()
        self.doc = parser.feed(content)
        parser.close()

    def get_document_title(self, default=''):
        doc_title = self.doc.find('.//title')
        if doc_title is None or doc_title.text is None:
            return default
        return utils.unescape_entities(utils.strip_spaces(doc_title.text))

    def get_title(self, default=''):
        title = self.doc.find('.//title')
        if title is None or title.text is None:
            return default
        return title.text

        #TODO correct detect parse artcile titles
        #titles_set = set()
        #title = utils.unescape_entities(utils.strip_spaces(title.text))
        #for headers in ['.//h1', './/h2', './/h3']:
        #    for el in list(self.doc.iterfind(headers)):
        #        if el is None:
        #            continue

        #        if el.text is not None and el.text:
        #            titles_set.add(el.text)
        #        if el.text_content():
        #            titles_set.add(el.text_content())

        #return sorted(titles_set, key=len)[-1]

    def get_paragraphs(self):
        paragraphs = []

        s_map = StatisticalMap(self.doc, for_tag='p')
        parent_container = s_map.guess_parent_container()
        if parent_container is None:
            return self.log.error('Cant find parent container for p')

        for parent, child in iterparent(parent_container):
            if child.tag != 'p':
                continue

            if child.find('.//a') is not None:
                child.attrib = {}
                text = ElementTree.tostring(
                    child, encoding='utf-8', method='html').decode('utf-8')
            else:
                text = get_text_of(child)

            if text is None:
                continue
            paragraphs.append(text)

        return paragraphs


class TextDocument(BaseDocument):
    def __init__(self, name, settings=None, **kw):
        self.name = name
        self._body = []

        self._settings = {
            'paragraph_margin_size': 2,
            'paragraph_indent_width': 2,
            'word_wrap_width': 80,
            'short_view_paragraphs': 2,
            'links_transform': True,
        }

        if settings is not None:
            self._settings.update(settings)

        self.formatters = formatter.FormatterManager()

    def _apply_formatters(self, to, text):
        formatted_text = text
        for fmt in self.formatters.iter_by(to):
            formatted_text = fmt(formatted_text, self._settings)
        return formatted_text

    def add_paragraph(self, text):
        self._body.append((self.formatters.PARAGRAPH, text))

    def add_title(self, text):
        self._body.append((self.formatters.TITLE, text))

    def _get_newlinw_sep(self):
        return os.linesep * self._settings['paragraph_margin_size']

    def view(self, short=False):
        body = []
        for n, (node_type, text) in enumerate(self._body):
            if short and n > self._settings['short_view_paragraphs']:
                break

            body_text = self._apply_formatters(node_type, text)
            if short and n == self._settings['short_view_paragraphs']:
                body_text = utils.truncate_text(body_text)
            body.append(body_text)

        newline_separator = (
            os.linesep * self._settings['paragraph_margin_size'])


        return newline_separator.join(body)

    def __str__(self):
        return self.view()

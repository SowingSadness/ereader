import re

from ereader.documents.utils import iterparent, get_text_of


class StatCounter(object):
    __slots__ = ('cnt_p', 'cnt_words', 'uuid')

    def __init__(self, size=1, text='', uuid=None):
        self.cnt_p, self.cnt_words = 0, 0
        self.inc_p(size)
        self.inc_words(text)

        self.uuid = uuid

    def inc_p(self, size=1):
        self.cnt_p += size

    def inc_words(self, text):
        self.cnt_words += len(re.findall(r'\b\w+\b', text, re.U | re.M))

    def __repr__(self):
        return '<{0}: paragraphs: {1}  words in: {2:>4} uuid: {3}>'.format(
            self.__class__.__name__, self.cnt_p, self.cnt_words, self.uuid)


class StatisticalMap(object):
    def __init__(self, tree, for_tag='p'):
        self.tree, self.for_tag = tree, for_tag

    def _get_statistical_map(self):
        stat_map = {}
        for parent, child in iterparent(self.tree):
            if child.tag != 'p':
                continue

            text = get_text_of(child)
            if text is None:
                continue

            parent_uuid = parent.attrib.get('uuid')
            if parent_uuid in stat_map:
                stat_map[parent_uuid].inc_p()
                stat_map[parent_uuid].inc_words(text)
            else:
                stat_map[parent_uuid] = StatCounter(0, text, parent_uuid)

        return stat_map

    def guess_parent_container(self):
        stat_map_sorted = sorted(
            self._get_statistical_map().items(),
            key=lambda x: x[1].cnt_words,
            reverse=True
        )

        frequent_parent_uuid, stat = stat_map_sorted[0]
        if not stat.cnt_p and not stat.cnt_words:
            return None

        for parent, child in iterparent(self.tree):
            if (parent.attrib.get('uuid') == frequent_parent_uuid):
                return parent

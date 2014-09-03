from __future__ import print_function, division, with_statement

from operator import and_, methodcaller
from itertools import ifilter, imap
from functools import partial
from collections import Counter
import os

class Text(object):
    def __init__(self, news_group, raw_data=None, _word_count=None):
        self.news_group = news_group
        self.raw_header, self.raw_text = raw_data.split("\n\n", 1) if raw_data is not None\
            else (None, None)
        self._word_count = _word_count

    def word_count(self):
        raw_words = ifilter(
            methodcaller('isalpha'),
            self.raw_text.split()
        )
        self._word_count = Counter(raw_words) if self._word_count is None\
            else self._word_count

        return self._word_count

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "Text(\n    {},\n    {}\n)".format(
            self.news_group,
            self.word_count()
        )

    def __add__(self, other):
        return Text(
            set([self.news_group, other.news_group]),
            None,
            _word_count=self.word_count()+other.word_count()
        )


def parse_data(data_path):
    """data_path : str
        Path to folder with newsgroups (training or test)
    """
    def parse_news_group(news_group):
        news_group_path = os.path.join(data_path, news_group)

        def parse_text(text_filename):
            text_path = os.path.join(news_group_path, text_filename)

            with open(text_path) as tf:
                return Text(news_group, tf.read())

        texts = imap(
            parse_text,
            os.listdir(news_group_path)
        )

        return texts

    data = chain.from_iterable(
        imap(
            parse_news_group,
            os.listdir(data_path)
        )
    )

    return data

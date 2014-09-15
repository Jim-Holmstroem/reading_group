from __future__ import print_function, division, with_statement

from operator import methodcaller, eq
from itertools import ifilter, imap, ifilterfalse, tee
from functools import partial
from collections import Counter
import os


class Text(object):
    def __init__(self, news_group, raw_data=None, _word_count=None):
        """
        news_group : set
        raw_data : str
        _word_count : Counter(str: int)
        """
        self.news_group = news_group
        self.raw_header, self.raw_text = raw_data.split("\n\n", 1) if raw_data is not None\
            else (None, None)
        self._word_count = _word_count

    def news_group(self):
        return self.news_group

    def word_count(self):
        """
        Returns
        -------
        _word_count : Counter(str: int)
        """
        def count(raw_text):
            raw_words = ifilter(
                methodcaller('isalpha'),
                raw_text.split()
            )
            raw_count = Counter(raw_words)

            return raw_count

        self._word_count = count(self.raw_text) if self._word_count is None\
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
            self.news_group | other.news_group,
            None,
            _word_count=self.word_count()+other.word_count()
        )


def parse_data(data_path):
    """
    data_path : str
        Path to folder with newsgroups (training or test)
    """
    def parse_news_group(news_group):
        news_group_path = os.path.join(data_path, news_group)

        def parse_text(text_filename):
            text_path = os.path.join(news_group_path, text_filename)

            with open(text_path) as tf:
                return Text(
                    frozenset({news_group}),
                    tf.read()
                )

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

class Bernoulli(object):
    def __call__(self, x):
        """
        Parameters
        ----------
        x : str

        Returns
        -------
        p_c : [float]
            p(x|c)
        """
        theta_c ** I(x_ij) * (1-theta_c) ** I(1-x_ij)
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "Ber(x|{theta})".format(
            theta=...
        )


class BagOfWords(object):
    def fit(self, texts):
        news_groups = partition(attrgetter('news_group') # :: [[Text]]
        news_groups_summary = map(
            partial(reduce, add),
            news_groups
        )
        return self  # TODO change this to more "functional"

    def predict(self, texts):
        def predict_one(text):
            return product(
                map(
                    self.word_models,
                    convert text.word_count().keys() # count_keys, all_words -> 0|1 \forall all_words "exists", exists(all_words)(keys())
                )  # alt. have {word: Ber(1, theta_wc)} and look them all up (and the rest is Ber(0, theta_wc))
            )

        return map(predict_one, texts)

def composition(f, *g):
    return (lambda *x: f(composition(*g)(*x))) if g else f


def partition(pred, iterator):
    """
    pred : A -> P
    iterator : [A]

    Returns
    -------
    : [[A]]
    """
    key_iterator, iterator = tee(iterator, 2)
    keys = list(set(imap(pred, key_iterator)))
    if len(keys) > 1:
        is_first_key = composition(partial(eq, keys[0]), pred)
        iterator_key, iterator_not_key = tee(iterator, 2)
        first_key_iterator = filter(is_first_key, iterator_key)
        not_first_key_iterator = list(ifilterfalse(is_first_key, iterator_not_key))
        return [first_key_iterator, ] +\
            partition(pred, not_first_key_iterator)

    else:
        return [list(iterator), ]


train_data = list(parse_data('data/20news-bydate-train/'))
test_data = list(parse_data('data/20news-bydate-test'))

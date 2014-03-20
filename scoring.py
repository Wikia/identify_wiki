from __future__ import division
from collections import defaultdict
from preprocessing import get_subdomain, preprocess, to_list


class Field(object):
    """Provides a standardized scoring metric for a set of NPs."""

    def __init__(self, data, is_url, use_tf, weight=1):
        """
        Instantiate a Field object that can return numerical scores for subject
        candidates.

        :param data: The phrase(s) to consider as part of the Field
        :type data: list or string

        :param is_url: Value indicating whether the data is a set of URLs
        :type is_url: boolean

        :param use_tf: Value indicating whether to build a term-frequency
            dictionary, otherwise binary is assumed
        :type use_tf: boolean

        :param weight: The number by which to multiply this Field's score
        :type weight: int
        """
        self.weight = weight
        self._max_score = None

        # Get lists of NPs or raw data, depending on the field
        if is_url:
            self.data = [get_subdomain(url) for url in to_list(data)]
        else:
            self.data = to_list(data)

        if use_tf:
            self._dict = self._build_tf_dict()
            self.score = self._score_tf
        else:
            self._dict = self._build_bin_dict()
            self.score = self._score_bin

    def _build_tf_dict(self):
        """
        Build a term-frequency dictionary containing terms and their counts.
        """
        if self.data:
            d = defaultdict(int)
            for term in self.data:
                normalized = preprocess(term)
                d[normalized] += 1
            if len(d.values()) > 0:
                self._max_score = max(d.values())
            return d
        return {}

    def _build_bin_dict(self):
        """
        Build a binary dictionary containing all terms and the value 1.0 to
        indicate their presence in the data set.
        """
        if self.data:
            return dict((preprocess(term), 1.0) for term in self.data)
        return {}

    def _score_tf(self, candidate):
        """
        Return a weighted term frequency score for a candidate, normalized by
        the greatest tf score in the dictionary.
        """
        if self._max_score is not None:
            return ((self._dict.get(candidate, 0.0) / self._max_score) *
                    self.weight)
        return 0.0

    def _score_bin(self, candidate):
        """
        Return a weighted binary score for a candidate.
        """
        return float(self._dict.get(candidate, 0.0)) * self.weight

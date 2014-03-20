import re
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def preprocess(text):
    """Convert strings into a canonical form usable as a key."""
    p = PorterStemmer()
    return tuple(re.sub('[^A-Za-z0-9]+', '', p.stem(word)) for word in
                 word_tokenize(text.lower()) if re.sub('[^A-Za-z0-9]+', '',
                                                       p.stem(word)) != '')


def to_list(terms):
    """Ensure that object is a list."""
    if terms is None:
        terms = []
    if isinstance(terms, (str, unicode)):
        terms = [terms]
    return terms


def build_dict_with_original_values(terms):
    """Given a list of terms, preprocess them and return a dict containing the
    normalized terms as keys, and lists of their corresponding original terms
    as values."""
    if not terms:
        return {}
    d = defaultdict(list)
    for term in terms:
        normalized = preprocess(term)
        d[normalized].append(term)
    for key in d:
        d[key] = list(set(d[key]))
    return d


def get_subdomain(url):
    """Given a URL, return the component most likely to be the subdomain (i.e.
    containing meaningful content)."""
    avoid = ['www', 'en', 'wikia', 'com', 'net']
    parts = url.split('.')
    for part in parts:
        if part not in avoid:
            return part
    return ''

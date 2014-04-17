from __future__ import division
import json
import requests
from nlp_services.wikia_utils import main_page_nps, phrases_for_wiki_field

from scoring import Field
from preprocessing import build_dict_with_original_values

# For ease of Field configuration
TEXT = False
URL = True
BINARY = False
TF = True

SOLR_ENDPOINT = 'http://search-s10:8983/solr/xwiki/select'


def identify_subject(wid, terms_only=False):
    """
    Identify subjects most likely to represent the content of a wiki.

    :param wid: The wiki ID for which to identify a subject
    :type wid: string

    :param terms_only: Whether to return only the subjects, as opposed to the
        terms preceded by the wiki ID and hostname
    :type terms_only: boolean

    :return: A comma-separated list of (wiki ID, hostname, and) best-matching
        subjects
    :rtype: string
    """

    # Request data from Solr
    params = {'q': 'id:%s' % wid,
              'fl': 'url,hostname_s,domains_txt,top_articles_txt,' +
                    'top_categories_txt,wiki_pagetitle_txt',
              'wt': 'json'}

    r = requests.get(SOLR_ENDPOINT, params=params)
    j = json.loads(r.content)
    docs = j['response']['docs']
    # Handle 0 docs response
    if not docs:
        if terms_only:
            return ''
        return wid
    response = docs[0]

    fields = {
        'hostname': Field(response.get('hostname_s'), URL, BINARY, 2),
        'domains': Field(response.get('domains_txt'), URL, TF, 1),
        'sitename': Field(
            phrases_for_wiki_field(wid, 'sitename_txt'), TEXT, BINARY, 1),
        'headline': Field(
            phrases_for_wiki_field(wid, 'headline_txt'), TEXT, BINARY, 1),
        'description': Field(
            phrases_for_wiki_field(wid, 'description_txt'), TEXT, TF, 1),
        'top_titles': Field(response.get('top_articles_txt'), TEXT, TF, 1),
        'top_categories': Field(
            response.get('top_categories_txt'), TEXT, TF, 1),
        'title_tag': Field(
            guess_from_title(response.get('wiki_pagetitle_txt')),
            TEXT, BINARY, 4)
        }

    # Build dictionary w/ preprocessed candidate keys and original term values
    candidates = main_page_nps(wid)
    [candidates.extend(fields[name].data) for name in fields]
    candidates = list(set(candidates))
    candidates = build_dict_with_original_values(candidates)

    def _score_candidate(candidate):
        return sum([fields[name].score(candidate) for name in fields])

    # Combine score of original candidate with scores of individual tokens
    total_scores = {}
    for candidate in candidates:
        total_score = _score_candidate(candidate)
        # Add scores of individual tokens, normalized by token count
        if len(candidate) > 1:
            token_score = 0
            for token in list(set(candidate)):
                token_score += _score_candidate((token,))
            token_score = token_score / len(candidate)
            total_score += token_score
        total_scores[candidate] = total_score

    # Sort candidates by highest score
    total_scores = sorted([(k, v) for (k, v) in total_scores.items() if 'wiki'
                           not in ''.join(k).lower()], key=lambda x: x[1],
                          reverse=True)

    # Return unstemmed forms of all candidates sharing the top score
    top_score = total_scores[0][1]
    top_terms = []
    top_stemmed = []
    for pair in total_scores:
        if pair[1] >= top_score:
            top_terms.append(candidates[pair[0]][0])
            top_stemmed.append(pair[0])
        else:
            break

    if terms_only:
        return ','.join(top_terms)
    return '%s,%s,%s' % (wid, response.get('hostname_s'), ','.join(top_terms))


def guess_from_title(title):
    """Given a title, return a list containing a single string representing the
    best guess for the wiki's subject, or an empty list if not possible."""
    if title is not None:
        low = title.lower()
        right = low.find('wiki')
        if right > 0:
            title = title[:right]
            low = low[:right]
            left = low.find('the ')
            if left > -1:
                title = title[left+4:]
                low = low[left+4:]
            if ' - ' in title:
                parts = title.split(' - ')
                i = min([(index, len(part)) for (index, part) in
                         enumerate(parts)], key=lambda x: x[1])[0]
                title = parts[i]
            return [title.strip().encode('utf-8')]
    return []

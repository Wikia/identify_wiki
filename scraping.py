import requests
import traceback
from bs4 import BeautifulSoup
from urllib2 import urlopen


def guess_from_title_tag(wid):
    """Given a wiki ID, return a list containing a single string representing
    the best guess for the wiki's subject, or an empty list if not possible."""
    response = requests.get('http://search-s10:8983/solr/main/select',
                            params={'q': 'wid:%s AND is_main_page:true' % wid,
                                    'fl': 'url', 'wt': 'json'})

    url = response.json().get('response', {}).get('docs', [{}])[0].get('url',
                                                                       None)
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        title = soup.title.string
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
    except:
        print traceback.format_exc()
    return []

if __name__ == '__main__':
    count = 0
    for line in open('topwams.txt'):
        count += 1
        if count > 100:
            break
        wid = line.strip()
        print guess_from_title_tag(wid)

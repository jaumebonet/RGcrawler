import re
import urllib2

from bs4.element import Tag
from bs4         import BeautifulSoup

from librarian import Manager


def isTagOrString(element):
    if isinstance(element, Tag):
        return (True, element)
    else:
        element = element.strip().strip(',').strip(u'\xb7').strip()
        return (False, str(element.encode('utf-8')))


def URL2soup(url):
    m = Manager()
    m.debug('Reading URL: {0}'.format(url))
    f = urllib2.urlopen(url)
    return BeautifulSoup(f.read())


def profile2name(text):
    return re.sub('_', ' ' , re.sub('\d+', '', text))


def researcher2publication(identifier):
    return {'identifier': identifier, 'primary': False, 'corresponding': False}

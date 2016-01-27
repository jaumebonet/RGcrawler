# -*-
#
# @author: jaumebonet
# @email:  jaume.bonet@gmail.com
# @url:    jaumebonet.github.io
#
# @date:   2016-01-19 15:43:53
#
# @last modified by:   jaumebonet
# @last modified time: 2016-01-27 16:58:34
#
# -*-
import re
import unicodedata

from bs4.element import Tag


def isTagOrString(element):
    if isinstance(element, Tag):
        return (True, element)
    else:
        element = element.strip().strip(',').strip(u'\xb7').strip()
        return (False, str(element.encode('utf-8')))


def profile2name(text):
    return normalizeText(re.sub('_', ' ' , re.sub('\d+', '', text)))


def researcher2publication(identifier):
    return {'identifier': identifier, 'primary': False, 'corresponding': False}


def normalizeText(text):
    if isinstance(text, str):
        return text
    text = text.strip()
    text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))
    return str(text)


def fixForcedLineChange(text):
    return text.replace('-\n', '').replace('\n', ' ')


def getStats(blob):
    return str(blob('div', attrs={'class': 'stats-count'})[0].contents[0].strip())

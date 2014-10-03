from bs4.element import Tag

import json
import re

from .helpers import isTagOrString


class Publication(object):

    pubURL   = 'https://www.researchgate.net/publication/{0}'
    typeATTR = ('span', {'class': 'publication-type'})
    ttleATTR = ('span', {'class': 'publication-title'})
    authATTR = ('div',  {'class': 'authors'})
    textATTR = ('a',    {'class': 'publication-preview'})
    abs1ATTR = ('div',  {'class': 'abstract'})
    abs2ATTR = ('span', {'class': 'full'})
    jrnlATTR = ('div',  {'class': 'details'})

    jrnlDATA = re.compile('([\S\s]*)(\d{2}\/\d+)([\s\S]*)')
    impcDATA = re.compile('(\d+\.\d{2})')

    def __init__(self, identifier, soup):
        p = Publication

        self.identifier = identifier
        self.type       = soup(p.typeATTR[0], attrs=p.typeATTR[1])[0].contents[0]
        self.type       = self.type.strip(':')
        self.title      = soup(p.ttleATTR[0], attrs=p.ttleATTR[1])[0].contents[0]
        self.title      = re.sub('\n', ' ', self.title).encode('utf-8')
        self.authors    = []
        self.available  = False
        self.journal    = {'name': None, 'volume': None, 'impact' : None}
        self.date       = None
        self.citations  = 0
        self.abstract   = None
        self.doi        = None
        self.pubmed     = None

        author = None
        for authors in soup(p.authATTR[0], attrs=p.authATTR[1]):
            for c in authors.contents:
                if isinstance(c, Tag):
                    author = int(c['href'].split('/')[-1].split('_')[0])
                    self.authors.append(author)
                else:
                    author = c.strip().strip(',').strip()
                    if author != '':
                        self.authors.append(author)

        textAct = soup(p.textATTR[0], attrs=p.textATTR[1])[0]['class']
        self.available = (not 'preview-not-available' in textAct)

        for i in soup(p.abs1ATTR[0], attrs=p.abs1ATTR[1]):
            for x in i(p.abs2ATTR[0], attrs=p.abs2ATTR[1])[0].contents:
                xbool, x = isTagOrString(x)
                if not xbool:
                    self.abstract = x

        jrnl = soup(p.jrnlATTR[0], attrs=p.jrnlATTR[1])[0]
        for x in jrnl.contents:
            xbool, x = isTagOrString(x)
            if x != '':
                print xbool
                print x
                if not xbool:
                    m = p.jrnlDATA.search(x)
                    self.journal['name']   = m.group(1).strip(';').strip()
                    self.journal['volume'] = m.group(3).strip(';').strip()
                    self.date = m.group(2).strip()
                else:
                    print x.contents[0]
                    self.journal['impact'] = p.impcDATA.search(x.contents[0]).group(1)

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, separators=(',', ': '))

import json

from librarian import Manager

from .helpers import isTagOrString
from .helpers import URL2soup
from .helpers import profile2name


class Researcher(object):

    baseURL  = "https://www.researchgate.net"
    prflURL  = "{0}/researcher/{1}"

    prflATTR = ('div', {'class': 'profile-header-personal'})
    nameATTR = ('a',   {'itemprop': "name"})
    instATTR = ('div', {'class': 'institution'})
    inf1ATTR = ('li',  {'class': 'publication-count'})
    inf2ATTR = ('li',  {'class': 'js-citation-stats'})
    ivalATTR = ('div', {'class': 'stats-count'})

    contributURL  = "{0}/profile/{1}/publications?sorting=newest&page={2}"

    m = Manager()

    def __init__(self, identifier = None, mainResearcher = False):
        r = Researcher

        self.identifier   = int(identifier)
        self.status       = 1  # 1 : RG account
                               # 0 : no account
                               # -1: private access

        self.boss         = False

        url  = r.prflURL.format(r.baseURL, identifier)
        soup = URL2soup(url)

        (self.profileName,
         self.status, self.name) = self._skimProfile(soup)

        (self.institution, self.department)         = (None, None)
        (self.pub_num, self.citations, self.impact) = (None, None, None)

        if mainResearcher:
            if self.status >= 0:
                (self.institution,
                 self.department) = self._skimInstitution(soup)

            if self.status == 1:
                (self.pub_num,
                 self.citations, self.impact) = self._skimImpact(soup)

    def _skimProfile(self, soup):
        r = Researcher
        try:
            data = soup(r.prflATTR[0], attrs=r.prflATTR[1])[0]
            try:
                r.m.info('Researcher with claimed RG profile.')
                p = data(r.nameATTR[0], attrs=r.nameATTR[1])[0]
                p = p['href'].split('/')[-1]
                return (p, 1, profile2name(p))
            except:
                r.m.info('Researcher has not claimed his/her RG profile.')
                p = data('a')[0]['href'].split('/')[-1]
                return (p, 0, profile2name(p))
        except:
            r.m.info('Access to this researcher\'s profile is not possible.')
            return (None, -1, None)

    def _skimInstitution(self, soup):
        r = Researcher
        try:
            for x in soup(r.instATTR[0], attrs=r.instATTR[1])[0].contents:
                tag, x = isTagOrString(x)
                if tag:
                    yield profile2name(x['href'].split('/')[-1])
                elif len(x.strip()) > 4:
                    yield x
        except:
            yield (None, None)

    def _skimImpact(self, soup):
        r = Researcher
        try:
            data = soup(r.inf1ATTR[0], attrs=r.inf1ATTR[1])[0]
            d = data(r.ivalATTR[0], attrs=r.ivalATTR[1])[0].contents[0].strip()
            yield int(d)
            data = soup(r.inf2ATTR[0], attrs=r.inf2ATTR[1])
            for RG in data:
                d = RG(r.ivalATTR[0], attrs=r.ivalATTR[1])[0].contents[0].strip()
                yield float(d) if '.' in d else int(d)
        except:
            yield (None, None, None)

    # PRIVATE METHODS
    def __str__(self):
        return json.dumps(self.__dict__, indent=2, separators=(',', ': '))

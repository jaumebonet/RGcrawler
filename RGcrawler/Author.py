# -*-
#
# @author: jaumebonet
# @email:  jaume.bonet@gmail.com
# @url:    jaumebonet.github.io
#
# @date:   2016-01-14 16:17:54
#
# @last modified by:   jaumebonet
# @last modified time: 2016-02-11 13:58:58
#
# -*-
import json

from pynion import Manager
from pynion import JSONer
from pynion import File
from pynion import Path

from .helpers import profile2name
from .helpers import normalizeText


m = Manager()
p = Path('authors')
siteURL    = "https://www.researchgate.net/"
authorURL  = siteURL + "researcher/{0}"
contribURL = siteURL + "profile/{0}/publications?sorting=newest&page={1}"


class Institution(JSONer):
    """docstring for Institution"""
    def __init__(self, soup):
        self._institution = normalizeText(
            soup('div', attrs={'class': 'institution-name'})[0].a.contents[0])
        self._department  = normalizeText(
            soup('div', attrs={'class': 'institution-dept'})[0].contents[0])


class Stats(JSONer):
    """docstring for Stats"""
    def __init__(self, soup):
        self._publications = int(self._get_stats(soup('li', attrs={'class': 'ga-publications-count'})[0]))
        self._citations    = int(self._get_stats(soup('li', attrs={'class': 'ga-citation-count'})[0]))
        self._impact       = float(self._get_stats(soup('li', attrs={'class': 'ga-impact-count'})[0]))

    def get_publications(self):
        return self._publications

    def _get_stats(self, blob):
        return str(blob('div', attrs={'class': 'stats-count'})[0].contents[0].strip())

    def got_all_contributions(self, contributions):
        return contributions >= self._publications


class Author(JSONer):
    """docstring for Author"""
    def __init__(self, identifier, soup):
        self._id            = int(identifier)
        self._name          = ""
        self._profile       = ""
        self._institution   = ""
        self._stats         = ""
        self._contributions = []
        self.get_identity_data(soup)

    def get_id(self):
        return self._id

    def get_profile(self):
        return self._profile

    def get_name(self):
        return self._name

    def get_contribution_count(self):
        return self._stats.get_publications()

    def add_contribution(self, contributionID):
        if contributionID not in self._contributions:
            self._contributions.append(contributionID)

    def get_url(self):
        return authorURL.format(self._id)

    def get_contributions_list_url(self, count):
        return contribURL.format(self._profile, count)

    def get_identity_data(self, soup):
        try:
            data = soup('div', attrs={'class': 'profile-header-personal'})[0]
            try:
                m.debug('Researcher with claimed RG profile.')
                p = data('a', attrs={'itemprop': "name"})[0]
                p = p['href'].split('/')[-1]
                self._profile     = p
                self._name        = profile2name(p)
                self._institution = Institution(soup('div', attrs={'class': 'institution-box'})[0])
                self._stats       = Stats(soup('ul', attrs={'class': 'stats-list'})[0])
            except:
                m.debug('Researcher has not claimed his/her RG profile.')
                p = data('a')[0]['href'].split('/')[-1]
                self._name = profile2name(p)
        except:
            m.debug('Access to this researcher\'s profile is not possible.')
            self._name = 'Unknown RG User'

    def has_all_contributions(self):
        return len(self._contributions) == self.get_contribution_count()

    @staticmethod
    def load_from_file(file_name):
        fd = open(file_name, 'r')
        a = Author.from_json(fd.read())
        fd.close()
        return a

    def store_to_file(self, file_name):
        fd = File(file_name, 'w')
        fd.open()
        fd.write(self.to_json())
        fd.close()

    def to_YAML(self):
        text  = "- name: {0}\n".format(self._name)
        text += "  id: {0}\n".format(self._id)
        return text

    # PRIVATE METHODS
    def __str__(self):
        data = self.to_dict(unpicklable=False, readable=True, api=True)
        return json.dumps(data, indent=2, separators=(',', ': '))

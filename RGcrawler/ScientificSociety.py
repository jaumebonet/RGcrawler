# -*-
#
# @author: jaumebonet
# @email:  jaume.bonet@gmail.com
# @url:    jaumebonet.github.io
#
# @date:   2016-01-19 13:06:47
#
# @last modified by:   jaumebonet
# @last modified time: 2016-02-10 18:40:58
#
# -*-
import json
import os
import urllib2

from bs4 import BeautifulSoup

from pynion import Manager
from pynion import JSONer
from pynion import Path
from pynion import File

from . import Author
from . import Contribution

m = Manager()


class SocietyManager(JSONer):
    """docstring for SocietyManager"""

    siteURL    = "https://www.researchgate.net/"
    authorURL  = siteURL + "researcher/{0}"
    contribURL = siteURL + "profile/{0}/publications?sorting=newest&page={1}"
    paperURL   = siteURL + "publication/{0}"

    def __init__(self):
        self._web_dir           = Path('web')
        self._authors_dir       = Path('authors')
        self._contributions_dir = Path('contributions')

    def get_author_dir(self):
        return self._authors_dir

    def get_author_data(self, authorID):
        url = self.author_url(authorID)
        alt = self.author_local(authorID)
        return self.get_data(url, alt)

    def get_contribution_list_data(self, authorID, count):
        url = self.contribution_list_url(authorID, count)
        alt = self.contribution_list_local(authorID, count)
        return self.get_data(url, alt)

    def get_contribution_data(self, contributionID):
        url = self.contribution_url(contributionID)
        alt = self.contribution_local(contributionID)
        return self.get_data(url, alt)

    def author_url(self, authorID):
        return SocietyManager.authorURL.format(authorID)

    def author_local(self, authorID):
        return os.path.join(self._web_dir.full, '{0}.author.web'.format(authorID))

    def author_json(self, authorID):
        return os.path.join(self._authors_dir.full, '{0}.json'.format(authorID))

    def get_contribution_dir(self):
        return self._contributions_dir

    def contribution_list_url(self, authorID, count):
        return SocietyManager.contribURL.format(authorID, count)

    def contribution_list_local(self, authorID, count):
        return os.path.join(self._web_dir.full, '{0}_{1}.contributionlist.web'.format(authorID, count))

    def contribution_url(self, contributionID):
        return SocietyManager.paperURL.format(contributionID)

    def contribution_local(self, contributionID):
        contributionID = contributionID.split('_')[0]
        return os.path.join(self._web_dir.full, '{0}.contribution.web'.format(contributionID))

    def contribution_json(self, contributionID):
        return os.path.join(self._contributions_dir.full, '{0}.json'.format(contributionID))

    def get_data(self, url, alt):
        if os.path.isfile(alt):
            return self.file2soup(alt)
        else:
            soup = self.url2soup(url)
            self.soup2file(soup, alt)
            return soup

    def url2soup(self, url):
        m.debug('Reading URL: {0}'.format(url))
        req  = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
        f    = urllib2.urlopen(req)
        soup = BeautifulSoup(f.read(), "html.parser")
        return soup

    def soup2file(self, soup, file_name):
        html = soup.prettify("utf-8")
        f = File(file_name, "w")
        f.open()
        f.write(html)
        f.close()

    def file2soup(self, file_name):
        m.debug('Reading file: {0}'.format(file_name))
        f    = open(file_name)
        soup = BeautifulSoup(f.read(), "html.parser")
        f.close()
        return soup


class ScientificSociety(JSONer):
    """docstring for ScientificSociety"""
    def __init__(self):
        self._manager       = SocietyManager()
        self._authors       = {}
        self._contributions = {}
        self.load()

    def load_author(self, authorID):
        authorID = int(authorID)
        if authorID not in self._authors:
            self._authors[authorID] = Author(authorID, self._manager.get_author_data(authorID))

    def load_contributions_of(self, authorID):
        authorID = int(authorID)
        self.load_author(authorID)
        count_page = 1
        while not self._authors[authorID].has_all_contributions():
            authorProfile = self._authors[authorID].get_profile()
            soup = self._manager.get_contribution_list_data(authorProfile, count_page)
            for pub in soup('li', attrs={'class': 'li-publication'}):
                identifier  = pub('a', {'class': 'ga-publication-item'})[0]["href"]
                identifier  = int(identifier.split('_')[0].split('/')[-1])
                author_list = []
                if identifier not in self._contributions:
                    self._contributions[identifier] = Contribution(identifier, pub)
                    cont_profile = self._contributions[identifier].get_profile()
                    author_list  = self._contributions[identifier].get_authors(pub, authorID)
                    moresoup     = self._manager.get_contribution_data(cont_profile)
                    self._contributions[identifier].get_more_content(moresoup)
                for aID in author_list:
                    self.load_author(aID)
                    self._authors[aID].add_contribution(identifier)
            count_page += 1

    def get_authors(self):
        return self._authors

    def authors2YAML(self, file_name):
        fd = File(file_name, 'w')
        fd.open()
        for author in self._authors:
            fd.write(self._authors[author].to_YAML())
        fd.close()

    def contributions2MD(self, exclude = None):
        for contid in self._contributions:
            if exclude is None or self._contributions[contid].get_type() not in exclude:
                fd = File(self._contributions[contid].get_short_profile() + '.md', 'w')
                fd.open()
                fd.write(self._contributions[contid].to_markdown(), 'utf-8')
                fd.close()

    def get_contributions(self):
        return self._contributions

    def is_empty(self):
        return len(self._contributions) == 0 and len(self._authors) == 0

    def save(self):
        for aID in self._authors:
            self._authors[aID].store_to_file(self._manager.author_json(aID))
        for cID in self._contributions:
            self._contributions[cID].store_to_file(self._manager.contribution_json(cID))

    def load(self):
        for file_name in self._manager.get_author_dir().list_files(pattern="*.json"):
            author = Author.load_from_file(file_name)
            self._authors[author.get_id()] = author
        for file_name in self._manager.get_contribution_dir().list_files(pattern="*.json"):
            contribution = Contribution.load_from_file(file_name)
            self._contributions[contribution.get_id()] = contribution

    # PRIVATE METHODS
    def __str__(self):
        data = self.to_dict(unpicklable=False, readable=True, api=True)
        return json.dumps(data, indent=2, separators=(',', ': '))

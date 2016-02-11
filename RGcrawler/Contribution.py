# -*-
#
# @author: jaumebonet
# @email:  jaume.bonet@gmail.com
# @url:    jaumebonet.github.io
#
# @date:   2016-01-14 17:33:47
#
# @last modified by:   jaumebonet
# @last modified time: 2016-02-10 18:42:43
#
# -*-
import json

from pynion import Manager
from pynion import JSONer
from pynion import File
from pynion import Path

from .helpers import isTagOrString
from .helpers import normalizeText
from .helpers import fixForcedLineChange

m = Manager()
p = Path('contributions')


class Contribution(JSONer):
    """docstring for Contribution"""
    def __init__(self, identifier, soup):
        self._id        = int(identifier)
        self._type      = ""
        self._title     = ""
        self._profile   = ""
        self._abstract  = ""
        self._authors   = []
        self._date      = ""
        self._journal   = {'name': None, 'volume': None, 'issue' : None, 'page': None}
        self._doi       = ""
        self._pubmed    = ""
        self._isbn      = ""
        self._citations = 0
        self.get_contribution_data(soup)

    def get_id(self):
        return self._id

    def get_type(self):
        return self._type

    def get_profile(self):
        return self._profile

    def get_short_profile(self):
        return "_".join(self._profile.split('_')[1:])

    def get_contribution_data(self, soup):
        self._type    = soup('span', {'class': 'publication-type'})[0].contents[0]
        self._type    = self._type.strip().lower().rstrip(':')
        self._title   = soup('span', {'class': 'publication-title'})[0].contents[0]
        self._title   = self._title.strip()
        self._profile = soup('a', {'class': 'ga-publication-item'})[0]["href"]
        self._profile = self._profile.split('/')[-1]
        self.get_abstract(soup)

    def get_authors(self, soup, authorID):
        if len(self._authors) == 0:
            for author in soup('div', attrs={'class': 'authors'})[0].contents:
                istag, content = isTagOrString(author)
                if not istag and len(content) > 0:
                    self._authors.append(authorID)
                elif istag:
                    content = content["href"].split('/')[-1].split('_')
                    self._authors.append(int(normalizeText(content[0])))
        return self._authors

    def get_abstract(self, soup):
        data = soup('div', {'class': 'abstract'})[0]('span', {'class': 'full'})[0]
        for content in data.contents:
            istag, content = isTagOrString(content)
            if not istag and len(content) > 1:
                self._abstract = fixForcedLineChange(content)

    def get_more_content(self, soup):
        self._date = self.meta_input(soup, 'citation_publication_date')
        if self._type == 'conference paper':
            self._journal['name'] = self.meta_input(soup, 'citation_conference_title')
        elif self._type == 'article':
            self._journal['name']   = self.meta_input(soup, 'citation_journal_title')
            self._journal['volume'] = self.meta_input(soup, 'citation_volume')
            self._journal['issue']  = self.meta_input(soup, 'citation_issue')
            self._journal['page']   = self.meta_input(soup, 'citation_firstpage')
            self._doi               = self.meta_input(soup, 'citation_doi')
            if len(soup('div', {'class': 'pub-source'})):
                self._pubmed = soup('div', {'class': 'pub-source'})[0]('a')[0]["href"]
                self._pubmed = self._pubmed.split('/')[-1]
        elif self._type == 'chapter':
            self._journal['name'] = self.meta_input(soup, 'citation_inbook_title')
            self._doi             = self.meta_input(soup, 'citation_doi')
            self._isbn            = self.meta_input(soup, 'citation_isbn')

        if len(soup('li', {'class': 'js-cited-in'})):
            data = soup('li', {'class': 'js-cited-in'})[0]
            self._citations = int(data('small')[0].contents[0].strip().strip('()'))

    def meta_input(self, soup, tag):
        if len(soup('meta', {'name': tag})) > 0:
            return soup('meta', {'name': tag})[0]["content"]
        else:
            return ""

    @staticmethod
    def load_from_file(file_name):
        fd = open(file_name, 'r')
        c  = Contribution.from_json(fd.read())
        fd.close()
        return c

    def store_to_file(self, file_name):
        fd = File(file_name, 'w')
        fd.open()
        fd.write(self.to_json())
        fd.close()

    def to_markdown(self):
        text  = "---\n"
        text += "layout: post\n"
        text += "title:  \"" + self._title + "\"\n"
        text += "date:   {0[0]}-{0[1]}-{0[2]}\n".format(self._date.strip().split('/'))
        text += "type: {0}\n".format(self._type)
        text += "authors: {0}\n".format(" ".join([str(x) for x in self._authors]))
        text += "---\n"
        text += normalizeText(self._abstract, return_string = False)
        return text

    def __str__(self):
        data = self.to_dict(unpicklable=False, readable=True, api=True)
        return json.dumps(data, indent=2, separators=(',', ': '))

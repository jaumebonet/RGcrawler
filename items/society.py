import atexit
import json
import os

from librarian import singleton
from librarian import Manager
from librarian import File

from .        import Researcher
from .        import Publication
from .helpers import URL2soup
from .helpers import researcher2publication as r2p


@singleton
class Society(object):

    publATTR = ('li', {'class': 'li-publication'})

    def __init__(self, mainAuthor, authorFile, publicationFile):

        # A manager for the Society
        self.m = Manager()
        self.m.info('A new scientific Society has been created.')

        # Content
        self.authors           = []
        self.author            = None
        self.authorUpdate      = True
        self.knownAuthors      = {}
        self.publications      = []
        self.knownPublications = {}

        # Data Files
        self.authorFile      = None
        self.publicationFile = None

        self._initFiles(authorFile, publicationFile)
        if self.author is None:
            self._addMainAuthor(mainAuthor)

    def isAuthorInSociety(self, identifier):
        return int(identifier) in self.knownAuthors.keys()

    def isPublicationInSociety(self, identifier):
        return int(identifier) in self.knownPublications.keys()

    def getAuthor(self, identifier):
        return self.authors[self.knownAuthors[identifier]]

    def getPublication(self, identifier):
        return self.publications[self.knownPublications[identifier]]

    def searchPublications(self, updateJournal):
        r   = Researcher
        url = '{0}/profile/{1}/publications?sorting=newest&page={2}'
        i   = 1
        while len(self.publications) < self.author['pub_num']:
            soup = URL2soup(url.format(r.baseURL, self.author['profileName'], i))
            for p in soup(self.publATTR[0], attrs=self.publATTR[1]):
                self._addPublication(p, updateJournal)
            i += 1

    def _addPublication(self, soup, updateJournal):
        identifier = int(soup['id'].split('_')[-1])
        if not self.isPublicationInSociety(identifier):
            self.m.info('Capturing new publication {0}.'.format(identifier))
            publication = Publication(identifier, soup)
            for i in range(len(publication.authors)):
                a = publication.authors[i]
                if isinstance(a, int):
                    a = self._trainAuthor(a)['identifier']
                else:
                    a = self.author['identifier']
                publication.authors[i] = r2p(a)
            publication.authors[-1]['corresponding'] = True
            self.publications.append(publication.__dict__)
            self.knownPublications[identifier] = len(self.publications) - 1
        else:
            self.m.info('Updating data of {0}'.format(identifier))

        publication = self.getPublication(identifier)
        # update PI and citation data
        

    def _initFiles(self, authorFile, publicationFile):
        self._openFile(ftype = 'authors',      filename = authorFile)
        self._openFile(ftype = 'publications', filename = publicationFile)

    def _addMainAuthor(self, identifier):
        ma = self._trainAuthor(identifier, mainAuthor = True)
        if self.author is not None:
            if ma == self.author:
                self.authorUpdate = False
            if ma['pub_num'] != self.author['pub_num']:
                n = ma['pub_num'] - self.author['pub_num']
                self.m.info('There are {0} new publications!'.format(n))
            if ma['citations'] != self.author['citations']:
                n = ma['citations'] - self.author['citations']
                self.m.info('There are {0} new citations!'.format(n))
            if ma['impact'] != self.author['impact']:
                n = ma['impact'] - self.author['impact']
                self.m.info('The impact factor is up by {0}!'.format(n))
        self.author = ma

    def _trainAuthor(self, identifier, mainAuthor = False):
        if not mainAuthor and self.isAuthorInSociety(identifier):
            ostring = 'Author {0} already belongs to the Society.'.format(identifier)
            self.m.info(ostring)
            return self.getAuthor(identifier)

        self.m.info('Getting data for author {0}.'.format(identifier))
        r = Researcher(identifier, mainAuthor).__dict__
        if not mainAuthor:
            self.authors.append(r)
            self.knownAuthors[r["identifier"]] = len(self.authors) - 1
        return r

    def _openFile(self, ftype, filename):
        if os.path.isfile(filename):
            self.m.info('A previous {0} registry is loaded'.format(ftype))
            fd = File(filename)
            if ftype == 'authors':
                self._loadAuthorRegistry(fd.readJSON())
            elif ftype == 'publications':
                self._loadPublicationRegistry(fd.readJSON())
            fd.close()
            fd.unregister()

        else:
            self.m.info('A new {0} registry is created'.format(ftype))
        if ftype == 'authors':
            self.authorFile = filename
            atexit.register(self._writeAuthorsFile)
        elif ftype == 'publications':
            self.publicationFile = filename
            atexit.register(self._writePublicationsFile)

    def _loadAuthorRegistry(self, jsonArray):
        self.authors = jsonArray
        self.author  = self.authors.pop(0)
        for i in range(len(self.authors)):
            self.knownAuthors[self.authors[i]['identifier']] = i

    def _loadPublicationRegistry(self, jsonArray):
        self.publications = jsonArray
        for i in range(len(self.publications)):
            self.knownPublications[self.publications[i]['identifier']] = i

    def _writeAuthorsFile(self):
        self.authors.insert(0, self.author)
        self.authorFile = File(self.authorFile, 'w')
        self.authorFile.write(json.dumps(self.authors, indent=2,
                                         separators=(',', ': ')))
        self.authorFile.close()

    def _writePublicationsFile(self):
        self.publicationFile = File(self.publicationFile, 'w')
        self.publicationFile.write(json.dumps(self.publications, indent=2,
                                              separators=(',', ': ')))
        self.publicationFile.close()

from librarian import Manager


# from .items import Researcher
from .items import Society

if __name__ == "__main__":

    m = Manager()
    m.set_stdout()
    m.set_detail()
    m.set_overwrite()

    RGid             = '15420125'
    society_file     = 'society.{0}.json'.format(RGid)
    publication_file = 'publications.{0}.json'.format(RGid)
    journal_file     = 'journals.{0}.json'.format(RGid)
    update_journal   = True

    society = Society(RGid, society_file, publication_file)
    society.searchPublications(update_journal)

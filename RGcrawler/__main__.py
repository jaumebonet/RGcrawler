# -*-
#
# @author: jaumebonet
# @email:  jaume.bonet@gmail.com
# @url:    jaumebonet.github.io
#
# @date:   2015-10-27 16:47:31
# @lab:    Correia's LPDI/EPFL
#
# @last modified by:   jaumebonet
# @last modified time: 2016-01-27 16:59:16
#
# -*-
from argparse import ArgumentParser

from pynion import Manager

from . import ScientificSociety

if __name__ == "__main__":

    m = Manager()
    m.set_stdout()
    m.set_detail()
    m.set_overwrite()

    parser = ArgumentParser()
    parser.add_argument("--authorID", dest="RGid", action="store", help="Query user ID")
    options = parser.parse_args()

    ss = ScientificSociety()
    ss.load_author(options.RGid)
    ss.load_contributions_of(options.RGid)
    ss.save()

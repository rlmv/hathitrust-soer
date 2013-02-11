
import glob
import os
import re

from pymarc import parse_xml_to_array

def retrieve_xml_paths():
    """ Generator over absolute filepaths to xml metadata files."""

    l = glob.iglob('./data/raw/*.xml')

    for x in l:
        yield os.path.abspath(x) 


def get_record_from_METS(fpath):
    """ Parse METS xml and return a pymarc record."""
    
    try:
        r = parse_xml_to_array(fpath)[0]
    except IndexError:
        r = None
    return r

""" 
From http://www.loc.gov/marc/bibliographic/bd260.html:

Subfield $c ends with a period (.), hyphen (-) for open-ended dates, 
a closing bracket (]) or closing parenthesis ()). If subfield $c is 
followed by some other subfield, the period is omitted. 
"""

PUB_REGEX = re.compile(r'[\d]{4})')
def normalize_pubyear(year):
    """ Attempt to normalize the publication year."""


if __name__ == "__main__":

    for p in retrieve_xml_paths():
        r = get_record_from_METS(p)
        print r.pubyear()



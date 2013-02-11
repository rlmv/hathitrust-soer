
import glob
import os
import re

from pymarc import parse_xml_to_array

def retrieve_xml_paths(x):
    """ Generator over absolute filepaths to xml metadata files."""

    l = glob.iglob(x)

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

YEAR_REGEX = re.compile(r'[\d]{4}')
""" 
This may need to be changed -- it won't deal with incomplete dates
like '19--' which I haven't seen recently, but may still be around.
"""

def normalize_year(year_string):
    """ Attempt to normalize a year string. 

    Returns the most recent year that can be extracted
    from year_string.
    """
    if not year_string:
        return None
    matches = YEAR_REGEX.findall(year_string)

    return int(max(matches, key=lambda s: int(s)))
  

if __name__ == "__main__":

    v = '../htrc/m/*.xml'
    x = './data/raw/*.xml'  

    for p in retrieve_xml_paths(v):
        r = get_record_from_METS(p)
        year = r.pubyear()

        print normalize_year(year)



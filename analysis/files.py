
import glob
import os
import re

from pymarc import parse_xml_to_array


def retrieve_xml_paths(target_dir):
    """ Generator over absolute filepaths for xml metadata files.

    Args:
        target_dir: path to directory containing xml files
    """
    target_dir = os.path.join(target_dir, '*.xml')
    l = glob.iglob(target_dir)

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
    return max(map(int, matches)) if matches else None

  

if __name__ == "__main__":

    v = '../htrc_api/m'
    x = './data/raw'  
    

    for p in retrieve_xml_paths(v):
        r = get_record_from_METS(p)
        year = r.pubyear()

        print normalize_year(year)
    print(normalize_year(None))


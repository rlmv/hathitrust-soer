

import re


def get_id_from_record(record):
    """ Extract the HathiTrust id from a pymarc record.

        Return None if no id."""
    try:
        htid = record['974']['a']
    except TypeError:
        htid = None
    return htid 


""" 
From http://www.loc.gov/marc/bibliographic/bd260.html:

Subfield $c ends with a period (.), hyphen (-) for open-ended dates, 
a closing bracket (]) or closing parenthesis ()). If subfield $c is 
followed by some other subfield, the period is omitted. 

The original REGEX:
YEAR_REGEX = re.compile(r'[\d]{4}') 
^^ it's too simple, and only catches complete 4-digit dates.
"""
YEAR_REGEX = re.compile(r'([\d]{4}|[\d]{3}|([\d]{2}(?![ ]?cm)))')
""" 

Okay, here are some possibilities that we have to deal with:
    186-?]
    [185-?]
    [189?]
    187?]
    184[5?]
    [186-]
    c19         -- is the 19th century, or a misinterpretaion of 260$c19 ?
    cl9l6]
    M. D. LXXIII.
    M. D. LXVIII.
    M.DCC.LXI.
    191
    18--
    18 -19
    MDCCLXXIX.
    MDCCLXX-LXXXIX]

    19 cm.        these get matched wrong
    5682 [1921]    as does this...

This new function covers the 2, 3, and 4 digit segmented cases.

Now to convert roman numerals...
There seem to be a number of cases of `l` being substituted for `1`.
"""

def normalize_year(year_string):
    """ Attempt to normalize a year string. 

    Returns the most recent year that can be extracted
    from year_string as an integer. 
    """
    # if not year_string:
    #     return None
    # matches = YEAR_REGEX.findall(year_string)

    # return max(map(int, matches)) if matches else None

    if not year_string:
        return None

    # l9l6 --> 1916
    year_string = year_string.replace('l', '1')
    
    matches = YEAR_REGEX.findall(year_string)
    if not matches:
        return None

    matches = map(lambda x: x[0], matches)        
    y = max(matches, key=lambda x: len(x))
    y = "{:0<4}".format(y) # ljust w/ 0s

    return int(y)


def normalize_subject(subj_string):
    """ Normalize a subject string.

    Current rules:
        - remove extraneous quotation marks
        - remove '[from old catalog]'
        - remove trailing periods and commas (not always correct though, in 
            instances like 'U.S.A.')
    """
    subj_string = subj_string.strip('\"\'')
    subj_string = subj_string.replace(" [from old catalog]", "")
    subj_string = subj_string.rstrip(",.")

    return subj_string
    


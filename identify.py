#!/usr/bin/env python

import argparse
from string import lower

from marc import MarcSQLite, get_id_from_record


def has_reference(record):
    for field in record.subjects():
        try:
            subj = lower(field.get_subfields('a')[0])   
            for term in terms:
                if term in subj:
                    return True
        except IndexError:
            pass
    return False

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A quick and dirty script for "
            "searching for keywords in a HathiTrust MARC database.")
    parser.add_argument('MARCDB',
                        help='A HathiTrust MarcSQLite database file from '
                        'which to retrieve records.')
    parser.add_argument('OUTFILE', 
                        help='File to write output to.')
    parser.add_argument('TERM',
                        nargs='+',
                        help='Search keywords.')
    

    args = parser.parse_args()

    terms = [lower(s) for s in args.TERM]

    m = MarcSQLite(args.MARCDB)

    with open(args.OUTFILE, 'w') as outfile:
        with m:
            for r in m.get_all_records():
                if has_reference(r):
                    id_ = get_id_from_record(r)
                    print id_
                    outfile.write("{}\n".format(id_))
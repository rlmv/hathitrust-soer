#!/usr/bin/env python

import json
import os
import argparse
import sys

from util import UnicodeWriter, file_id_iter
from marc import map_subjects, map_publication_years, MarcSQLite


def map_onto_records(func, db, csv_fname, json_fname=None, 
                ids=None, sort_by_value=False):
    """ Run a mapping over the metadata db.

        func - should return a dictionary
        db - open record database
        file_stub - write serialized results here, in 
            .json and .csv formats. 
        ids - an iterable of HathiTrust ids to map over. If None, all 
            records in the database are retrieved.
        sort_by_value - default: False --> sort by key
    """

    if not ids:
        records = db.get_all_records()
    else:
        records = db.get_records(ids) 
        records = filter(lambda x: x, records) # discard Nones..

    mapped = func(records)

    if json_fname:
        with open(json_fname, 'w') as f:
            json.dump(mapped, f)

    f = lambda x: x[1 if sort_by_value else 0]
    mapped_list = sorted(mapped.items(), key=f)

    with open(csv_fname, 'w') as f:
        csvwriter = UnicodeWriter(f, quoting=csv.QUOTE_ALL)
        for key, val in mapped_list:
            csvwriter.writerow([unicode(key), unicode(val)])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("ANALYSIS", 
        choices=['years', 'subjects'], 
        help="Type of analysis to perform/information to extract. "
        "'years' tallies the publication years of all documents. "
        "'subjects' accumulates the subjects of the documents.")
    parser.add_argument("DATABASE", 
        help="MarcSQLite record database from which to pull records.")
    parser.add_argument("CSV_OUT", 
        help="File for writing CSV output.")
    parser.add_argument("--json", "-j", 
        metavar="JSON_OUT",
        dest="JSON_OUT",
        help="Output a JSON result file in addition the the default csv file.")
    parser.add_argument("--id-file", "-i", 
        metavar="ID_FILE", 
        dest="ID_FILE", 
        help="Analyze the ids contained in ID_FILE rather than the entire database.")

    args = parser.parse_args()

    if not os.path.exists(args.DATABASE):
        print "database {} does not exist".format(args.DATABASE)
        sys.exit()

    with MarcSQLite(args.DATABASE) as db:

        if args.ID_FILE:
            ids = file_id_iter(args.ID_FILE)
        else:
            ids = None

        if args.MAPPING == 'years':
            mapper = map_publication_years
        elif args.MAPPING == 'subjects':
            mapper = map_subjects

        map_onto_records(mapper, db, args.CSV_OUT, json_fname=args.JSON_OUT, 
            ids=ids)


        




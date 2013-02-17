
import json
import csv

from util import UnicodeWriter
from metadata import map_subjects, map_publication_years, MarcSQLite


#-----change this as needed-------
DB_STUB = 'results/non_google.20111101_01'
#---------------------------------

def map_onto_records(func, db, file_stub, ids=None, sort_by_value=False):
    """ Run a mapping over the metadata db.

        func - should return a dictionary
        db - open record database
        file_stub - write serialized results here, in 
            .json and .csv formats. 
        ids - an iterable of HathiTrust ids to map over. If None, all 
            records in the database are retrieved.
        sort_by_value - default: False --> sort by key
    """

    json_fname = file_stub + ".json"
    csv_fname = file_stub + ".csv"

    if not ids:
        records = db.get_all_records()
    else:
        ids = map(lambda x: x.strip(), ids) #? need this??
        records = db.get_records(ids) 
        records = filter(lambda x: x, records) # discard Nones..

    mapped = func(records)

    with open(json_fname, 'w') as f:
        json.dump(mapped, f)

    f = lambda x: x[1 if sort_by_value else 0]

    mapped_list = sorted(mapped.items(), key=f)

    with open(csv_fname, 'w') as f:
        csvwriter = UnicodeWriter(f, quoting=csv.QUOTE_ALL)
        for key, val in mapped_list:
            csvwriter.writerow([unicode(key), unicode(val)])


if __name__ == "__main__":

    dbname = DB_STUB + ".db"
    subj_fname = DB_STUB + "_subjects"
    years_fname = DB_STUB + "_years"

    with MarcSQLite(dbname) as db:

        with open('results/non_google_nz.txt', 'r') as f:
            htids = f.readlines()
        years_fname = 'results/non_google_nz_years'

        map_onto_records(map_publication_years, db, years_fname, ids=htids)
        #map_onto_records(map_subjects, db, subj_fname)
        





import json
import csv

from metadata import map_subjects, map_publication_years, MarcSQLite


# change this as needed
DB_STUB = '../non_google.20111101_01'


def map_onto_records(func, db, file_stub, sort_by_value=False):
    """ Run a mapping over the metadata db.

        func - should return a dictionary
        db - open record database
        file_stub - write serialized results here, in 
            .json and .csv formats. 
        sort_by_value - default: False --> sort by key
    """

    json_fname = file_stub + ".json"
    csv_fname = file_stub + ".csv"

    mapped = func(db.get_all_records())

    with open(json_fname, 'w') as f:
        json.dump(mapped, f)

    i = 1 if sort_by_value else 0
    f = lambda x: [i]
    mapped_list = sorted(mapped.items(), key=f)

    with open(csv_name, 'w') as f:
        csvwriter = csv.writer(f)
        for key, val in mapped_list:
            csvwriter.writerow([key, val])


if __name__ == "__main__":

    dbname = DB_STUB + ".db"
    subj_fname = DB_STUB + "_subjects"
    years_fname = DB_STUB + "_years"

    with MarcSQLite(dbname) as db:

        map_onto_records(map_subjects, db, subj_fname)
        map_onto_records(map_publication_years, db, years_fname)





import json
import csv
import codecs
import cStringIO

from metadata import map_subjects, map_publication_years, MarcSQLite


#-----change this as needed-------
DB_STUB = 'non_google.20111101_01'
#---------------------------------

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

    with open(csv_fname, 'w') as f:
        csvwriter = UnicodeWriter(f)
        for key, val in mapped_list:
            csvwriter.writerow([unicode(key), unicode(val)])



class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.

    From http://docs.python.org/2/library/csv.html
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == "__main__":

    dbname = DB_STUB + ".db"
    subj_fname = DB_STUB + "_subjects"
    years_fname = DB_STUB + "_years"

    with MarcSQLite(dbname) as db:

        map_onto_records(map_subjects, db, subj_fname)
        map_onto_records(map_publication_years, db, years_fname)




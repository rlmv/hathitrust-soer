
import cStringIO
import sqlite3 as sqlite

from pymarc import parse_xml_to_array

from records import get_id_from_record


def parse_xml_to_SQLite(xml_file, sqlite_name, strict=False, normalize_form=None):
    """ Parse a single file collection of xml metadata, and
        store it in a SQLite database. 

        This is function to use if you are trying to convert a 
        HathiTrust dataset file into a managable format."""

    handler = SQLiteXmlHandler(sqlite_name, strict, normalize_form)
    parse_xml(xml_file, handler)


class MarcSQLite(object):
    """ SQLite wrapper for storing pymarc.Record objects."""

    def __init__(self, db_fname):
        self.fname = db_fname
        self._conn = None

        # set up
        self.open_conn()
        self._execute('''CREATE TABLE IF NOT EXISTS records 
                             (id TEXT, record TEXT)''')
        self.close_conn()

    def __enter__(self):
        self.open_conn()
        return self

    def __exit__(self, *exc):
        self.close_conn()

    def open_conn(self):
        if not self._conn:
            self._conn = sqlite.connect(self.fname)

    def close_conn(self):
        self._conn.close()
        self._conn = None


    def insert_record(self, record):
        """ Insert a serialize xml representation of the pymarc record
            into the database, keyed by id """
        htid = get_id_from_record(record)
        print htid
        xml = record_to_xml(record)
        self._execute('''INSERT OR REPLACE INTO records
                             VALUES (?, ?)''', [htid, xml])
        self._commit()


    def select_record(self, htid):
        """ Select a pymarc.Record object from the database."""
        
        cur = self._execute('''SELECT record FROM records
                                   WHERE id = ?''', [htid])
        r = cur.fetchone()
        if not r:
            return None
        record = parse_xml_string_to_record(r[0])

        return record


    def get_all_ids(self):
        """ Return an iterator over all ids in the database."""

        cur = self._execute('''SELECT id FROM records''')
        for x in cur:
            yield x[0]


    def get_all_records(self):
        """ Return an iterator over all records in the database."""

        cur = self._execute('''SELECT record FROM records''')
        for y in cur:
            record = parse_xml_string_to_record(y[0])
            yield record


    def _commit(self):
        self._conn.commit()

    def _execute(self, statement, params=None): 
        if not params:
            params = []
        return self._conn.execute(statement, params)


def parse_xml_string_to_record(xmlstring):
    """ Parse an xml string and return a pymarc.Record object. """

    xml_io = cStringIO.StringIO(xmlstring)
    record = parse_xml_to_array(xml_io)[0]
    return record

import os
import glob
import re
import StringIO
import sqlite3 as sqlite
from collections import Counter

from lxml import etree
import pymarc
from pymarc import parse_xml, parse_xml_to_array, XmlHandler, Record, record_to_xml



from pathfinder import PairTreePathFinder


class SQLiteXmlHandler(XmlHandler):
    """ Subclass of XMLHandler providing a direct write to an SQLite 
        database.
    """

    def __init__(self, sqlite_db, strict=False, normalize_form=None):

        self.sqlite_db = MarcSQLite(sqlite_db)
        ## Old style form here - pymarc is 2.x
        XmlHandler.__init__(self, strict=strict, 
                            normalize_form=normalize_form)


    def process_record(self, record):
        print "inserting"
        with self.sqlite_db as db:
            db.insert_record(record)
        

class MarcSQLite(object):
    """ SQLite wrapper for storing pymarc.Record objects."""

    def __init__(self, db_fname):
        self.fname = db_fname
        self.open_conn()
        self._execute('''CREATE TABLE IF NOT EXISTS records 
                             (id TEXT, record TEXT)''')

    def __enter__(self):
        if not self.conn:
            self.open_conn()
        return self

    def __exit__(self, *exc):
        self.close_conn()

    def open_conn(self):
        self.conn = sqlite.connect(self.fname)
        #self.conn.text_factory = unicode # serialization is not in unicode.

    def close_conn(self):
        self.conn.close()
        self.conn = None

    def _commit(self):
        self.conn.commit()

    def _execute(self, statement, *params): 
        return self.conn.execute(statement, *params)


    def insert_record(self, record):
        """ Insert a serialize MARC21 representation of the pymarc record
            into the database, keyed by id """
        htid = get_id_from_record(record)
        # serialized = record.as_marc()
        # serialized = serialized.decode('utf-8')
        xml = record_to_xml(record)
        print xml
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
        buff = StringIO.StringIO(r[0])
        record = parse_xml_to_array(buff)[0]

        return record

    def get_all_ids(self):
        """ Return an iterator over all ids in the database."""

        cur = self._execute('''SELECT id FROM records''')
        for x in cur:
            yield x[0]


def get_id_from_record(record):
    """ Extract the HathiTrust id from a pymarc record.

        Return None if no record."""
    try:
        htid = record['974']['a']
    except TypeError:
        htid = None
    return htid


def parse_xml_to_SQLite(xml_file, sqlite_name, strict=False, normalize_form=None):

    handler = SQLiteXmlHandler(sqlite_name, strict, normalize_form)
    parse_xml(xml_file, handler)


def retrieve_xml_paths_from_dir(target_dir):
    """ Generator over a directory of xml metadata files.

    Args:
        target_dir: path to directory containing xml files
    """
    target_dir = os.path.join(target_dir, '*.xml')
    l = glob.iglob(target_dir)

    for x in l:
        yield os.path.abspath(x) 


def retrieve_METS_paths_from_pairtree(doc_ids, root):
    """ Extract METS meta data from pairtree collection rooted at 'root'

    Args:
    - doc_ids:iterable of document ids to extracte
    - root of the HathiTrust collection

    Returns:
        A generator over absolute file paths.
    """
    pf = PairTreePathFinder(root)

    for x in doc_ids:
        path, post = pf.get_path_to_htid(x)
        mpath = os.path.join(path, post + '.mets.xml')
        yield mpath

def get_MARC_by_id(doc_ids, marc_path):
    """ Generate pymarc representaions of MARC records from a single 
        file.

        Args:
        - doc_ids: ids for which to retrieve records
        - marc_path: path to the MARC file
    """

    records = pymarc.parse_xml_to_array(marc_path)
    for r in records:
        yield r


""" 
From http://www.loc.gov/marc/bibliographic/bd260.html:

Subfield $c ends with a period (.), hyphen (-) for open-ended dates, 
a closing bracket (]) or closing parenthesis ()). If subfield $c is 
followed by some other subfield, the period is omitted. 
"""

YEAR_REGEX = re.compile(r'[\d]{4}')
""" 
This regex may need to be changed -- it won't deal with incomplete dates
like '19--' which I haven't seen recently, but may still be around.
"""

def normalize_year(year_string):
    """ Attempt to normalize a year string. 

    Returns the most recent year that can be extracted
    from year_string as an integer. 
    """
    if not year_string:
        return None
    matches = YEAR_REGEX.findall(year_string)
    return max(map(int, matches)) if matches else None


def get_records_from_meta(fpath):
    """ Parse marc xml and return an array of pymarc records."""
    
    r = parse_xml_to_array(fpath)
    return r

  
def map_publication_years(records):
    """ Map the publication years of a collection into a dictionary. 

    This will produce year:number pairs, which relates the number of
    documents published in a given year to that year. Years are integers.

    Args: 
    -collection :  an iterator over pymarc Record objects.
    """

    mapping = Counter()

    for r in records:
        year = r.pubyear()
        year = normalize_year(year)

        mapping[year] += 1

    return mapping


def map_subjects(records):
    """ Map subjects of the collection into a dictionary.

        I `believe` this is the best way to implement this, and that
        subject names always live in the 'a' subfield. 

        Should the keys be lowercased? 
    """

    mapping = Counter()

    for r in records:
        for f in r.subjects():
            subj_name = f.get_subfields('a')[0]
            mapping[subj_name] += 1

    return mapping


if __name__ == "__main__":

    # v = '../htrc_api/m'
    # x = './data/raw'  

    # paths = retrieve_xml_paths_from_dir(v)
    # records = [get_records_from_meta(p)[0] for p in paths]
    # # for r in records:
    # #     print normalize_year(r.pubyear())
    
    # print map_publication_years(records)
    # print map_subjects(records)

    # l = [u'dul1.ark:/13960/t0000w70p',
    #      u'dul1.ark:/13960/t0000wr88',
    #      u'dul1.ark:/13960/t0000x309',
    #      u'dul1.ark:/13960/t0000xw9z',
    #      u'dul1.ark:/13960/t0000xx6z',
    #      u'dul1.ark:/13960/t0000z95t',
    #      u'dul1.ark:/13960/t0000zd2q',
    #      u'dul1.ark:/13960/t0000zg6j']



    # for r in get_MARC_by_id(l, '../non_google.20111101_01.xml'):
    #     print r.title()
    #     print r['947']['a

    #parse_xml_to_SQLite('../non_google.20111101_01.xml', 'test.db')

    with MarcSQLite('test.db') as db:
         print db.select_record('dul1.ark:/13960/t0ks7fx1m')
         for id_ in db.get_all_ids():
            print id_




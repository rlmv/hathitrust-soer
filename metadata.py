
import os
import glob
import re
import cStringIO
import sqlite3 as sqlite
from collections import Counter

from pymarc import parse_xml, parse_xml_to_array, XmlHandler, record_to_xml

from pathfinder import PairTreePathFinder


def parse_xml_to_SQLite(xml_file, sqlite_name, strict=False, normalize_form=None):
    """ Parse a single file collection of xml metadata, and
        store it in a SQLite database. 

        This is function to use if you are trying to convert a 
        HathiTrust dataset file into a managable format."""

    handler = SQLiteXmlHandler(sqlite_name, strict, normalize_form)
    parse_xml(xml_file, handler)


class SQLiteXmlHandler(XmlHandler):
    """ Subclass of pymarc.XmlHandler providing a direct write to an SQLite 
        database.
    """

    def __init__(self, sqlite_db, strict=False, normalize_form=None):

        self.sqlite_db = MarcSQLite(sqlite_db)
        ## Old style form here - pymarc is 2.x
        XmlHandler.__init__(self, strict=strict, 
                            normalize_form=normalize_form)


    def process_record(self, record):
        with self.sqlite_db as db:
            db.insert_record(record)
        

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
        """ Insert a xml representation of the pymarc record
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


    def get_records(self, ids):
        """ Return an iterator over the records cooresponding to ids.

            If an id is not in the database, return None. """
        for htid in ids:
            r = self.select_record(htid)
            yield r


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


def get_id_from_record(record):
    """ Extract the HathiTrust id from a pymarc record.

        Return None if no id."""
    try:
        htid = record['974']['a']
    except TypeError:
        htid = None
    return htid 


## DB, XML ^^^
##----------------------------------------------------------------------
## analysis, mapping vvv

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
        norm_year = normalize_year(year)
        mapping[norm_year] += 1

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
            try:
                subj = f.get_subfields('a')[0]
                subj = normalize_subject(subj)
                mapping[subj] += 1
            except IndexError:
                pass

    return mapping


def get_xml_paths_from_dir(target_dir):
    """ Iterator over a directory of xml metadata files.

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


    # parse_xml_to_SQLite('../non_google.20111101_01.xml', 
    #     '../non_google.20111101_01.db')

    # with MarcSQLite('../non_google.20111101_01.db') as db:
    #     for r in db.get_all_records():
    #         print r.title()
    

    # l = ["Magnetic induction.", 
    #      "Maine (Battleship) [from old catalog]",
    #      '"Mallery, Garrick,"',
    #      '"Mammoth cave, Ky. [from old catalog]"']

    # for x in l:
    #     print normalize_subject(x)

    # l = [None, 
    #     "186-?]", 
    #     "[185-?]",
    #     "[189?]",
    #     "187?]", 
    #     "1898", 
    #     "184[5?]", 
    #     "[186-]]",
    #     "18 -19", 
    #     "1"]

    # for i in l:
    #     print i, normalize_year(i)

    with MarcSQLite('results/non_google.20111101_01.db') as db:
        for r in db.get_all_records():
            # year = r.pubyear()
            # nyear = normalize_year(year)
            # if not nyear or nyear > 2000:
            #     print year, " ::: ", nyear

            if r['655']:
                print r['655']['a']







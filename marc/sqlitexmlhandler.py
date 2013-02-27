
from pymarc import XmlHandler

from marcsqlite import MarcSQLite


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
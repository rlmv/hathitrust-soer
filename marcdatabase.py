#!/usr/bin/env python

import argparse

from marc import parse_xml_to_SQLite


""" 
Command line tool to parse a HathiTrust MarcXML file and
construct a MarcSQLite database.

Usage:
    build_db_from_xml.py non_google.xml 
        ---> constructs non_google.db
    build_db_from_xml.py non_google.xml mydatabase.db
        ---> constructs mydatabase.db
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=
        "Command line tool to parse a HathiTrust " 
        "MarcXML file into a SQLite database.")

    parser.add_argument("SOURCE_XML", 
        help="A multi-record MarcXML file.")
    parser.add_argument("TARGET_DB", 
        help="Name of database to create.")

    args = parser.parse_args()

    source = args.SOURCE_XML
    target = args.TARGET_DB
    
    parse_xml_to_SQLite(source, target)


    
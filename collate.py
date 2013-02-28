#!/usr/bin/env python3

import argparse
import sys
import os

from util import file_id_iter, require_py3
from remove_running_headers.bigcollate import bigcollate


if __name__ == "__main__":

    require_py3()

    parser = argparse.ArgumentParser(description="A command line wrapper \
        around Ted Underwood's collation package.")

    parser.add_argument('COLLECTION', 
                        help='Specifies the root directory of a HathiTrust collection.')
    parser.add_argument('ID_FILE', 
                        nargs='?', 
                        default=False, 
                        help='File of HathiTrust ids to collate; defaults to the entire collection.')
    parser.add_argument('--rewrite-existing',
                        action='store_true',  
                        help='Overwrite existing collated documents.')
    parser.add_argument('--no-divs', 
                        action='store_true', 
                        help='If specified, do not write page or header divisions to the collation.')
    parser.add_argument('--skip', 
                        type=int,
                        default=0,
                        help='Number of lines in the id file to skip; eg after an interrupted collate.')
    args = parser.parse_args()
    
    collection = args.COLLECTION
    rewrite_existing = args.rewrite_existing
    include_divs = not args.no_divs
    id_file = args.ID_FILE

    if not id_file:
        # default identifier in collection
        id_file = os.path.join(collection, 'id')
        
    ids = file_id_iter(id_file)
    print(bigcollate(ids, collection, rewrite_existing=rewrite_existing, 
        include_divs=include_divs, skip=args.skip))



os.path.join(os.path.expanduser("~"), ".collate_resume")




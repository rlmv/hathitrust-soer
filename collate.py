
import argparse
import sys
import os

from remove_running_headers.bigcollate import bigcollate

class VersionError(Exception): pass

def file_iter(fname, mode='r'):
    """ Iterator over stripped lines in a file."""
    with open(fname, mode) as f:
        for line in f:
            yield line.strip()


if __name__ == "__main__":

    if sys.version_info[0] != 3:
        raise VersionError("requires Python 3")

    parser = argparse.ArgumentParser(description="A command line wrapper \
        around Ted Underwood's collation package.")

    parser.add_argument('COLLECTION', 
                        help='root directory of the HathiTrust collection')
    parser.add_argument('ID_FILE', 
                        nargs='?', 
                        default=False, 
                        help='file of HathiTrust ids to collate; defualts to the entire collection')
    parser.add_argument('--rewrite-existing',
                        action='store_true',  
                        help='Overwrite existing collated documents.')
    parser.add_argument('--no-divs', 
                        action='store_true', 
                        help='If present, do not write page or header divisions to the collation.')
    args = parser.parse_args()
    
    collection = args.COLLECTION
    rewrite_existing = args.rewrite_existing
    include_divs = not args.no_divs
    id_file = args.ID_FILE

    if not id_file:
        # default identifier in collection
        id_file = os.path.join(collection, 'id')
        
    ids = file_iter(id_file)
    bigcollate(ids, collection, rewrite_existing=rewrite_existing, 
        include_divs=include_divs)






import argparse
import sys

class VersionError(Exception): pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A command line wrapper \
        around Ted Underwood's collation package.")

    parser.add_argument('COLLECTION', 
                        help='root directory of the HathiTrust collection')
    parser.add_argument('--rewrite-existing', 
                        help='Overwrite existing collated documents.')

    args = parser.parse_args()
    
    if sys.version_info[0] != 3:
        raise VersionError("requires Python 3")


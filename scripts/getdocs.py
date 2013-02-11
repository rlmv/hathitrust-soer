#! /usr/local/bin/python

import sys
import os
import argparse
from string import replace

from requests.exceptions import RequestException

from dataclient.htdataclient import HTDataClient as HTDC  
from oauth_keys import client_key, client_secret

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="An interactive document retriever for the HathiTrust data API.")
    parser.add_argument('targetdir', metavar='DIR',
        help="Retrieved files are stored in this directory.")

    args = parser.parse_args()
    if not os.path.exists(args.targetdir):
        raise Exception("Target directory does not exist.")

    htdc = HTDC(client_key, client_secret)

    try:
        while True:
            s = raw_input("Enter target htid >> ")

            try:
                r = htdc.getaggregate(s)
            except RequestException as re:
                print "Error with request: {}".format(re)
                continue    

            # convert to valid file name
            fname = replace(s, ':', '+')
            fname = replace(fname, '/', '=')
            fname = fname + '.zip'
            print "fname: {}".format(fname)

            fpath = os.path.join(args.targetdir, fname)

            with open(fpath, 'w') as f:
                f.write(r)

    except KeyboardInterrupt:
        print '/n'
        sys.exit()
            
            
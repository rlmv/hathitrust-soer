#! /usr/local/bin/python

import sys
import json
import argparse
from cStringIO import StringIO
from zipfile import ZipFile

from hathitrust_api.solr_api import SolrAPI


def main(args):
    
    """ Implements a command line tool that performs queries against
        the HTRC Solr Proxy."""
    
    # ToDo: refactor...
    
    parser = argparse.ArgumentParser(
                        description="A command line tool for the HTRC Solr Proxy.")
    
    parser.add_argument('querystring',
                        metavar='QUERY',
                        help='a Solr query string')
    
    parser.add_argument('-f', '--fields',
                        metavar='FIELD',
                        nargs='*',
                        help='fields to include with the results')
    
    parser.add_argument('-o', '--outfile',
                        default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='optional output file')
    
    parser.add_argument('-n', '--numfound',
                        action='store_true',
                        help='number of results matching QUERY')
    
    parser.add_argument('-i', '--ids',
                        action='store_true',
                        help='return documents identifiers only')
    
    parser.add_argument('-m', '--marc',
                        type=lambda x: ZipFile(x, 'w'),
                        metavar='MARCFILE', help='retrieve MARC records and write to zip file')
    
    # arguments to implement:   
    #                           max - specify a maximum number of results to retrieve.
    #                           pretty - pretty output
    # deal with mutually exclusive blocks.
    
    
    args = parser.parse_args(args)
    outfile = args.outfile

    solr = SolrAPI()
    
    try: 
        if args.numfound:
            numfound = solr.getnumfound(args.querystring)
            outfile.write("{}\n".format(numfound))
        
        elif args.ids:
            for doc_id in solr.getallids(args.querystring):
                outfile.write("{}\n".format(doc_id))
                
        elif args.marc:
            marcfile = args.marc
            for doc_ids in solr.batch_ids(args.querystring):
                marcs = getmarc(doc_ids)
                # there's probably a faster way to merge multiple zip
                # files together...
                with ZipFile(StringIO(marcs)) as z:
                    for name in z.namelist():
                        marcfile.writestr(name, z.read(name))
                
        # regular query:
        else:
            _first = True # need to wrangle with the formatting...
            outfile.write('{ "results" : [\n')
            
            for doc in solr.iterquery(args.querystring, fields=args.fields):    
                if _first:
                    _first = not _first
                else:
                    outfile.write(",\n")
                
                # lets format this so the output is readable
                pretty = json.dumps(doc, indent=4)
                outfile.write("{}".format(pretty))
                
            outfile.write('\n]}')
            

    ## We probably need to catch HTTP errors here...
    
    except KeyboardInterrupt:
        sys.exit()
                
    finally:
        if outfile is not sys.stdout:
            outfile.close()
        try:
            args.marc.close()
        except AttributeError:
            pass


if __name__ == "__main__":
    main(sys.argv[1:])

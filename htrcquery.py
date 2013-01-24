

import sys
import json
import argparse

from solr.solrproxy import iterquery, getnumfound, getallids


if __name__ == "__main__":
    
    """ Implements a command line tool that performs queries against
        the HTRC Solr Proxy."""
    
    parser = argparse.ArgumentParser(
                        description="This is a command line tool for the HTRC Solr Proxy.")
    parser.add_argument('querystring', metavar='QUERY',
                        help='a Solr query string')
    parser.add_argument('--fields', metavar='FIELD', nargs='*',
                        help='fields to include with the results')
    parser.add_argument('-o', '--outfile', default=sys.stdout, type=argparse.FileType('w'),
                        help='file to write the output to')
    parser.add_argument('-n', '--numfound', action='store_true',
                        help='output the total number of results found by this query')
    parser.add_argument('-i', '--ids', action='store_true',
                        help='only output the document ids')
    
    # arguments to implement:   marc retriever - exclusive from --fields and -n
    #                           xml option
    #                           max - specify a maximum number of results to retrieve.
    #                           pretty - pretty output
    # deal with mutually exclusive blocks.
    
    
    args = parser.parse_args()
    
    try: 
        print args
        
        if args.numfound:
            numfound = getnumfound(args.querystring)
            args.outfile.write("{}\n".format(numfound))
        
        elif args.ids:
            for doc_id in getallids(args.querystring):
                args.outfile.write("{}\n".format(doc_id))
                
        # elif marc:
        #       ...
        # regular query:
        # do these results need to be wrapped in a dict or list?
        else: 
            for doc in iterquery(args.querystring, fields=args.fields):
                # lets format this so the output is readable
                pretty = json.dumps(doc, indent=4)
                args.outfile.write("{}\n".format(pretty))
                
    ## We need to catch HTTP errors here.
                
    finally:
        if args.outfile is not sys.stdout:
            args.outfile.close()

    

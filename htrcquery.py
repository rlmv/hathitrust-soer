#! /usr/local/bin/python

import sys
import json
import argparse
from cStringIO import StringIO
from zipfile import ZipFile

from solr.solrproxy import iterquery, getnumfound, getallids, getmarc


def batch_ids(querystring, num=10):
    """ Returns lists of ids for querystring of
        at most length [num]."""
    
    g = getallids(querystring)
    batch = []
    while True:
        
        try:
            doc_id = g.next()
            batch.append(doc_id)
            if len(batch) == num:
                yield batch
                # new batch
                batch = []
                
        except StopIteration:
            # give up what's left
            yield batch
            return 
            

def main(argv):
    
    """ Implements a command line tool that performs queries against
        the HTRC Solr Proxy."""
    
    # can we make it so that the querystring is input without surrounding
    # quotation marks?
    
    # ToDo: refactor...
    
    parser = argparse.ArgumentParser(
                        description="This is a command line tool for the HTRC Solr Proxy.")
    parser.add_argument('querystring', metavar='QUERY',
                        help='a Solr query string')
    parser.add_argument('-f', '--fields', metavar='FIELD', nargs='*',
                        help='fields to include with the results')
    parser.add_argument('-o', '--outfile', default=sys.stdout, type=argparse.FileType('w'),
                        help='write output to this file')
    parser.add_argument('-n', '--numfound', action='store_true',
                        help='list the total number of results returned by this query')
    parser.add_argument('-i', '--ids', action='store_true',
                        help='output a stream of document ids')
    parser.add_argument('-m', '--marc', type=lambda x: ZipFile(x, 'w'),
                        metavar='MARCFILE', help='retrieve MARC records and write to zip file')
    
    # arguments to implement:   marc retriever - exclusive from --fields and -n
    #                           xml option
    #                           max - specify a maximum number of results to retrieve.
    #                           pretty - pretty output
    # deal with mutually exclusive blocks.
    
    
    args = parser.parse_args(argv[1:])
    outfile = args.outfile
    
    try: 
        if args.numfound:
            numfound = getnumfound(args.querystring)
            outfile.write("{}\n".format(numfound))
        
        elif args.ids:
            for doc_id in getallids(args.querystring):
                outfile.write("{}\n".format(doc_id))
                
        elif args.marc:
            marcfile = args.marc
            for doc_ids in batch_ids(args.querystring):
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
            
            for doc in iterquery(args.querystring, fields=args.fields):    
                if _first:
                    _first = not _first
                else:
                    outfile.write(",\n")
                
                # lets format this so the output is readable
                pretty = json.dumps(doc, indent=4)
                outfile.write("{}".format(pretty))
                
            outfile.write('\n]}')
            
    ## We need to catch HTTP errors here.
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
    main(sys.argv)

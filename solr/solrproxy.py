
import sys
import json
import argparse

import requests
try:
    from lxml import etree
except ImportError:
    import xml.etree.cElementTree as etree
    


SOLR_HOST = "http://chinkapin.pti.indiana.edu"
SOLR_PORT = 9994
SOLR_STUB = "/solr/select/"
solrbaseurl = "".join([SOLR_HOST, ":", str(SOLR_PORT), SOLR_STUB])


def query(querystring, rows=10, start=0, fields=[], json=True):
    """
    Arguments:
        rows: the maximum number of results to return
        fields: an iterable of fields to return with the
            response, eg. fl=['title', 'author']
        json: true by default  - returns the JSON object,
            or, if false, returns an xml tree.

    Return:
        JSON resource, or lxml etree.
    """
    terms = {}
    terms['q'] = querystring
    terms['rows'] = rows
    terms['start'] = start
    terms['qt'] = 'sharding'

    if json:
        terms['wt'] = 'json'

    if fields:
        terms['fl'] = ','.join(fields)

    r = requests.get(solrbaseurl, params=terms)
    r.raise_for_status()

    if json:
        return r.json()

    return etree.fromstring(r.content)


def iterquery(querystring, rows=10, fields=[]):
    """ Defines an generator over a query.
    
        This lets you stick the query in a for loop
        and iterate over all the results, like so:
        
        >>> for doc in iterquery(<querystring>):
        ...     print json.dumps(doc, indent=4)
        
        The return docs are python-interpreted json
        structures - the SOLR api spec defines the
        available fields:
        http://wiki.htrc.illinois.edu/display/COM/2.+Solr+API+User+Guide
        
        For now, errors get passed up from the query
        function...TODO: implement some handling.
    """
    
    num_retrieved = 0
    new_iter = True
    num_found = None
    
    """" need to iteate over ['response']['docs']"""
    
    while True:
        # send a query, then iterate over ['response']['docs']
        result = query(querystring, rows=rows, start=num_retrieved, fields=fields, json=True)
        
        if new_iter:
            num_found = result['response']['numFound']
            new_iter = False
        
        if num_found == num_retrieved:
            raise StopIteration
            
        for doc in result['response']['docs']:
            num_retrieved += 1
            
            yield doc



def jsonquery():
    pass

def xmlquery():
    pass


def getnumfound(querystring):
    """ Return the total number oqf matches for the query. """
    return int(query(querystring, rows=0, json=True)['response']['numFound'])


def getmarc():
    base = "http://chinkapin.pti.indiana.edu:9994/solr/MARC/?volumeIDs="

    ids = ['mdp.39015062319309', 'mdp.39015026997125', 'uc1.31822021576848']
    idstring = "|".join(volid for volid in ids)
    
    url = base + idstring
    print url
    r = requests.get(url)
    r.raise_for_status()
    
    with open('marc.zip', 'wb') as f:
        f.write(r.content)


#s = "author : marchm*"
#print getnumfound(query(s, json=True))
##print json.dumps(query(s, json=True), indent=4)
#for i,doc in enumerate(iterquery(s, rows=10, fields = ['id'])):
#    print i+1
#    print json.dumps(doc)



#querystring = 'title: new zealand'
##q = query(querystring, rows=100, fields=['title', 'htsource'], json=True)
#
## docs = q['response']['docs']
## for doc in docs:
#
#
#print "{} public domain records found.".format(getnumfound(q))
#
## ids = parseIDs(q)
## for id in ids:
##     print id
#
##print getnumfound(q)
#print json.dumps(q, indent=4)
#
#getallIDs(querystring, 'test.txt')


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
    # arguments to implement:   marc retriever - exclusive from --fields and -n
    #                           xml option
    #                           max - specify a maximum number of results to retrieve.
    #                           pretty - pretty output
    args = parser.parse_args()
    print args
    
    ## We need a try-except block around this to catch HTTP errors. 
    
    if args.numfound:
        numfound = getnumfound(args.querystring)
        args.outfile.write("{}\n".format(numfound))
    # elif marc:
    #       ...
    # regular query:
    else: 
        for doc in iterquery(args.querystring, fields=args.fields):
            # lets format this so the output is readable
            pretty = json.dumps(doc, indent=4)
            args.outfile.write("{}\n".format(pretty))   
            
            
    # this is kind of bad - argparse doesn't open the filein a context
    # manager, so we need some try finally work to make sure this closes
    args.outfile.close()
    



## Command line tools:


##### `getdocs.py`

An example tool built using the [hathitrust-api] Data API to retrieve HathiTrust aggregate resources. It is limited to retrieving public domain documents, and requires an OAuth keyset to use--see `oauth_keys.py.template` for information about how to set up the `oauth_keys.py` file.

Usage:

```
python getdocs.py [-h] TARGETDIR [IDFILE]

An interactive document retriever for the HathiTrust Data API.

positional arguments:
  TARGETDIR   Retrieved files are stored in this directory.
  IDFILE      Path to a file of HathiTrust identifiers.

optional arguments:
  -h, --help  show this help message and exit
```

`TARGETDIR` specifies the directory into which to save downloaded resources. `IDFILE` is an optional argument, specifying the path to a file containing HathiTrust document identifiers, one per line. If `IDFILE` is not specified the program runs under an interactive prompt.

With `IDFILE`:
	
	python getdocs.py . target_ids.txt
	
Interactive:
	
	python getdocs.py .

	Enter target htid >> dul1.ark:/13960/t0000xw9z
	loc.ark+=13960=t01z49n4f.zip saved to .

	Enter target htid >>


##### `solrquery.py`

A more useful example using the [hathitrust-api][ht api] Solr API, `solrquery.py` is a command line interface with the HTRC's Solr index, allowing document searches and MARC retrieval.

Usage:
```	
python solrquery.py [-h] [-f [FIELD [FIELD ...]]] [-o OUTFILE] [-n] [-i]
                    [-m MARCFILE]
                    QUERY

A command line tool for the HTRC Solr Proxy.

positional arguments:
  QUERY                 A Solr query string. See http://wiki.htrc.illinois.edu
                        /display/COM/Solr+Proxy+API+User+Guide for details.

optional arguments:
  -h, --help            show this help message and exit
  -f [FIELD [FIELD ...]], --fields [FIELD [FIELD ...]]
                        A subset of index fields to include with the results.
  -o OUTFILE, --outfile OUTFILE
                        Use --outfile to specify and optional output file.
  -n, --numfound        Print the number of results matching QUERY.
  -i, --ids             Return a stream of documents identifiers only.
  -m MARCFILE, --marc MARCFILE
                        Retrieve MARC records for all documents matching QUERY
                        and write a zip archive to MARCFILE.
```



##### `marcdatabase.py`

Tool for converting a large HathiTrust XML file to a managable SQLite database format, accessible through the class `marc.MarcSQLite`.

Usage:

```
python marcdatabase.py [-h] SOURCE_XML TARGET_DB

Command line tool to parse a HathiTrust MarcXML file into a SQLite database.

positional arguments:
  SOURCE_XML  A multi-record MarcXML file.
  TARGET_DB   Name of database to create.

optional arguments:
  -h, --help  show this help message and exit
```



##### `analyze.py`

Various analysis functions over the records in a MarcSQLite database.

```
python analyze.py [-h] [--json JSON_OUT] [--id-file ID_FILE]
              {years,subjects} DATABASE CSV_OUT

positional arguments:
  {years,subjects}      Type of analysis to perform/information to extract.
                        'years' tallies the publication years of all
                        documents. 'subjects' accumulates the subjects of the
                        documents.
  DATABASE              MarcSQLite record database from which to pull records.
  CSV_OUT               File for writing CSV output.

optional arguments:
  -h, --help            show this help message and exit
  --json JSON_OUT, -j JSON_OUT
                        Output a JSON result file in addition the the default
                        csv file.
  --id-file ID_FILE, -i ID_FILE
                        Analyze the ids contained in ID_FILE rather than the
                        entire database.
```

##### `identify.py`

Tool for identifying documents in a MarcSQLite database via metadata features and keywords.

Usage:
```
python identify.py [-h] MARCDB OUTFILE TERM [TERM ...]

A quick and dirty script for searching for keywords in a HathiTrust MARC
database.

positional arguments:
  MARCDB      A HathiTrust MarcSQLite database file from which to retrieve
              records.
  OUTFILE     File to write output to.
  TERM        Search keywords.

optional arguments:
  -h, --help  show this help message and exit
```


##### `collate.py` (Python 3!)

A command line wrapper around Ted Underwood's document collation scripts.

Usage:

```
python3 collate.py [-h] [--rewrite-existing] [--no-divs] [--skip SKIP]
                  COLLECTION [ID_FILE]

A command line wrapper around Ted Underwood's collation package.

positional arguments:
  COLLECTION          Specifies the root directory of a HathiTrust collection.
  ID_FILE             File of HathiTrust ids to collate; defaults to the
                      entire collection.

optional arguments:
  -h, --help          show this help message and exit
  --rewrite-existing  Overwrite existing collated documents.
  --no-divs           If specified, do not write page or header divisions to
                      the collation.
  --skip SKIP         Number of lines in the id file to skip; eg after an
                      interrupted collate.
```

##### `ocreval.py` (Python 3!)

Command line version of Ted Underwood's OCR evaluation scripts.

Usage:

```
python3 ocreval.py [-h] COLLECTION OUTFILE [IDFILE]

positional arguments:
  COLLECTION  Path to a HathiTrust collection.
  OUTFILE     Desination file for CSV output.
  IDFILE      Optional file of HathiTrust identifiers to evaluate. Defaults to
              the entire collection.

optional arguments:
  -h, --help  show this help message and exit
```


## Classes and functions:
Bits and pieces for working with HathiTrust MARC XML records. Check the docstrings for more usage information.

###### marc.MarcSQLite  
Class for storing HathiTrust MARC records in a SQLite database schema.
###### marc.parse_xml_to_SQLite
Main function for parsing a HathiTrust MARC record to a MarcSQLite accessible database.
###### marc.normalize_year
###### marc.normalize_subject
###### marc.map_publication_years
###### marc.map_subjects
###### pairtree.PairTreePathFinder


#### Dependencies:
Code in this package depends on the following third party libraries:

* [requests]
* [requests-oauthlib]
* [ptree]
* [pymarc]

They should all be installable with a `pip <dependency>` command. There may still be an issue with the requests-oauthlib version in PyPI. If you have issues using `hathitrust_api.DataAPI`, install it from the [source][requests-oauthlib].

####Submodules: 
Due to issues involving Python 3, and needing to hack into some existing code, I've included several packages as submodules to ease the pain of setting up a bunch of dependencies. If you do a `git clone`, these will all be included:

* [hathitrust-api]
* [remove-running-headers]
* [ocreval]
	
[requests]: http://docs.python-requests.org/en/latest/
[requests-oauthlib]: http://github.com/requests/requests-oauthlib
[ptree]: http://github.com/edsu/ptree
[pymarc]: http://github.com/edsu/pymarc
[hathitrust-api]: http://github.com/rlmv/hathitrust-api
[remove-running-headers]: http://github.com/rlmv/remove-running-headers
[ocreval]: http://github.com/rlmv/ocreval

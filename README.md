

### Modules:


* ##### `getdocs.py`

	An example tool built using the [hathitrust-api] Data API to retrieve HathiTrust aggregate resources. It is limited to retrieving public domain documents, and requires an OAuth keyset to use--see `oauth_keys.py.template` for information about how to set up the `oauth_keys.py` file.
	
	Usage:

		python getdocs.py [-h] TARGETDIR [IDFILE]

	`TARGETDIR` specifies the directory into which to save downloaded resources. `IDFILE` is an optional argument, specifying the path to a file containing HathiTrust document identifiers, one per line. If `IDFILE` is not specified the program runs under an interactive prompt.

	With `IDFILE`:
		
		python getdocs.py . target_ids.txt
		
	Interactive:
		
		python getdocs.py .

		Enter target htid >> dul1.ark:/13960/t0000xw9z
		loc.ark+=13960=t01z49n4f.zip saved to .

		Enter target htid >>


* ##### solrquery.py

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
	
	Examples:
	
		


	

	
* ##### marcdatabase.py

	Tool for converting a large HathiTrust XML file to a managable SQLite database format, accessible through the class `marc.MarcSQLite`.

* ##### map.py

	Various analysis functions over the records in a MarcSQLite database.

* ##### identify.py
	
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


* ##### collate.py (\*Py3*)
	
	A command line wrapper around Ted Underwood's document collation package.

* ##### ocreval.py (\*Py3*)
	
	Command line version of Ted Underwood's ocrevaluation package.


####Dependencies:
Code in this package depends on these third party libraries:

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
	
[requests]: docs.python-requests.org/en/latest/
[requests-oauthlib]: github.com/requests/requests-oauthlib
[ptree]: github.com/edsu/ptree
[pymarc]: github.com/edsu/pymarc
[hathitrust-api]: github.com/rlmv/hathitrust-api
[remove-running-headers]: github.com/rlmv/remove-running-headers
[ocreval]: ithub.com/rlmv/ocreval

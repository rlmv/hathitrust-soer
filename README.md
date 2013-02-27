

###Modules:
* _getdocs.py_

	An example tool built using the [hathitrust-api][ht api] Data API to retrieve HathiTrust aggregate resources. It is limited to retrieving public domain documents, and requires an OAuth keyset to use--see `oauth_keys.py.template` for information about how to set up the `oauth_keys.py` file.

		python getdocs.py [-h] TARGETDIR [IDFILE]

	`TARGETDIR` specifies the directory into which to save downloaded resources. `IDFILE` is an optional argument, specifying the path to a file containing HathiTrust document identifiers, one per line. If `IDFILE` is not specified the program runs under an interactive prompt.

	With `IDFILE`:
		
		python getdocs.py ./ target_ids.txt
		
	Interactive:
		
		python getdocs.py ./ 

		Enter target htid >> dul1.ark:/13960/t0000xw9z
		loc.ark+=13960=t01z49n4f.zip saved to .

		Enter target htid >>


* _solrquery.py_
	
	Another example 
* _marcdatabase.py_
* map.py
* identify.py
* collate.py (*Py3*)
* ocreval.py (*Py3*)

[ht api]: github.com/rlmv/hathitrust-api

####Included submodules: 


####Dependencies:
* requests
* requests-oauthlib
* sklearn
* pymarc
* ptree

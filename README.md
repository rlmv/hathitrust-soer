hathitrust-client
=================

hathitrust-client is an interface for the HathiTrust APIs. Currently contains some basic classes that can be used to acces both the Bibliographic API and the Data API. At the moment the methods are just simple URI wrappers, but there's certainly room for expansion.

If you want to use the Data API, you need to get an OAuth keyset from HathiTrust.


Packages:
---------
* requests (you can get it straight out of PyPI)
* requests-oauthlib (a Requests plugin; the version in PyPI currently has some errors, so get it straight from the source repo here: https://github.com/requests/requests-oauthlib)
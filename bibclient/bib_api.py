

__author__ = 'robertmarchman'

import urllib2, json

BIB_BASEURL = 'http://catalog.hathitrust.org/api/volumes/'

ID_TYPES = ['oclc',
			'lccn',
			'issn',
			'isbn',
			'htid',
			'recordnumber',
			]

REQUEST_TYPES = ['json']


class HTBib(object):

	def __init__(self):
		pass


	def _bib_url_single(self, id_type, id_value, full=False, request_type='json'):
		""" 
		Build a single identifier url from the passed parameters

		:param id_type: string from ID_TYPES
		:param id_value: identifier of type id_type
		:param full: toggles full/brief 
		:param request_type: HathiTrust currently only supports json requests.

		"""
		
		if full == False:
			detail = 'brief' 
		else:
			detail = 'full'

		url = "".join([BIB_BASEURL, detail, "/", id_type, "/", id_value, '.json'])
		return url


	def single_bib_request(self, id_type, id_value, full=False):

		url = self._bib_url(id_type, id_value, full)
		r = urllib2.urlopen(url)
		return json.load(r)


if __name__ == "__main__":
	
	bquery = HTBib()
	js = bquery.bib_request('htid', 'mdp.39015012849165', full=True)
	print json.dumps(js, indent=2)
	print js['records'].keys()


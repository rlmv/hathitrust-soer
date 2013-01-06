
__author__ = 'robertmarchman'

import requests
import json   

from constants import BIB_BASEURL

class HTBibInterface(object):

    def _multi_id_url(self, id_dictionary, full=False, return_type='json'):
        """ 
        :param id_dictionary: an iterable of dictionary entries, with the id value (string) keyed by
        the id type (can be int or string). Eg:
            ids = [{id:1, oclc:45678}, {lccn:70628581}]
        See the HathiTrust bib API documentation for more details, and information
        on the id:MyID tag. 

        :param full: specifes full/brief detail - full includes MARCXML fields.
        :param return_type: currently json is the only type available

        """

        if full == False:
            detail = 'brief' 
        else:
            detail = 'full'

        search_string = "|".join([";".join([key + ":" + str(spec[key]) 
            for key in spec]) for spec in id_dictionary])
        url = "".join([BIB_BASEURL, detail, '/', return_type, '/', search_string])

        return url


    def get_single_record_json(self, id_type, id_value, full=False):
        """
        Returns the pythonic interpretation of the HathiTrust JSON record
        for the <id_type>:<id_value> pair. 
        See the API for specific details of the returned structure.

        :param id_type: string from ID_TYPES
        :param id_value: identifier of type id_type
        :param full: toggles full/brief - MARCXML

        Note that this method calls the multi_record method, however the
        returned results are formatted as specified in the single record section of the API.
        """

        spec = "REQ"

        id_dict = [{id_type:id_value, "id":spec}]
        multi_request = self.get_multi_record_json(id_dict, full=full)

        return multi_request[spec]


    def get_multi_record_json(self, id_dictionary, full=False):
        """
        Returns records for the requests in id_dictionary. To conform to the HathiTrust
        API, the size of id_dictionary should be limited to 20.

        :param id_dictionary: an iterable of dictionaries, with the id value (string) keyed by
        the id type (can be int or string). Eg:
            ids = [{id:1, oclc:45678}, {lccn:70628581}]
        See the HathiTrust bib API documentation for more details, and information
        on the id:MyID persistant identifier tag.

        :param full: specifes full/brief detail -- full includes MARCXML fields.

        """

        req_url = self._multi_id_url(id_dictionary, full=full)

        r = requests.get(req_url)
        r.raise_for_status()
        return r.json()





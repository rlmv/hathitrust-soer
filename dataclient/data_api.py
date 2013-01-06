

__author__ = 'robertmarchman'

import requests
import json
import xml.etree.ElementTree as ET


from requests_oauthlib import OAuth1
from constants import DATA_BASEURL, SECURE_DATA_BASEURL


class HTDataInterface(object):

    def __init__(self, client_key, client_secret, secure=False):
        """ Initialize a HTDataInterface object.

        Args:
            client_key: OAuth client key (registered with HathiTrust)
            client_secret: secret OAuth key
            secure: toggles http/https session. Defaults to
                 http, use https for access to restricted content.

        Initializes a persistent Requests session and attaches 
        OAuth credentials to the session. All queries are performed as 
        method calls on the HTDataInterface object.

        """

        self.client_key = client_key
        self.client_secret = client_secret
        self.oauth = OAuth1(client_key=client_key, 
                            client_secret=client_secret, 
                            signature_type='query')

        self.rsession = requests.Session()
        self.rsession.auth = self.oauth

        if secure:
            self.baseurl = SECURE_DATA_BASEURL
        else: 
            self.baseurl = DATA_BASEURL


    def _make_request(self, resource, doc_id, sequence=None, 
                        v=1, json=False, callback=None):
        """ Construct and perform URI request.

        Args:
            resource: resource type
            doc_id: document identifier of target
            sequence: page number for single page resources
            v: API version 
            json: if json=True, the json representation of
                the resource is returned. Only valid for resources that 
                are xml or xml+atom by default.
            callback: optional javascript callback function, 
                which only has an effect if json=True.

        Returns: 
            requests response object

        Note there's not much error checking on url construction, 
        but errors do get raised after badly formed requests.

        """

        url = "".join([self.baseurl, resource, '/', doc_id])
        
        if sequence:
            url += '/' + str(sequence)

        params = {'v': str(v)}
        if json:
            params['alt'] = 'json'
            if callback:
                params['callback'] = callback

        r = self.rsession.get(url, params=params)
        r.raise_for_status()

        return r


    def get_meta(self, doc_id, json=False):
        """ Retrieve Volume and Rights Metadata resources.

        Args:
            doc_id: document identifier
            json: if json=True, the json representation of
                the resource is returned, otherwise efaults to an atom+xml 
                format.

        Return: 
            ...

        """
        return self._make_request('meta', doc_id, json=json)


    def get_structure(self, doc_id, json=False):
        """ Retrieve a METS document.

        Args:
            doc_id: target document
            json: toggles json/xml 
        Return:
            xml or json string

        """
        return self._make_request('structure', doc_id, json=json)


    def get_pagemeta(self, doc_id, seq, json=False):
        """ Retrieve single page metadata. """
        return self._make_request('pagemeta', doc_id, sequence=seq, json=json)


    def get_aggregate(self, doc_id):
        """ Return aggregate record data. 

        Return: 
            zip content that contains tiff/jp2/jpeg, .txt OCR files,
                + Source METS (not the same as Hathi METS)

        """
        return self._make_request('aggregate', doc_id)


    def get_pageimage(self, doc_id, seq):
        """ Retrieve Single Page Image.

        Return:
            response with tiff, jp2, or jpeg file

        """
        return self._make_request('pageimage', doc_id, sequence=seq)


    def get_pageocr(self, doc_id, sequence):
        """ 
        Return:
            UTF-8 encoded OCR plain text

        """
        return self._make_request('pageimage', doc_id, sequence=sequence)


    def get_pagecoordocr(self, doc_id, sequence):
        """
        Return:
            UTF-8 encoded XML OCR

        """
        return self._make_request('pagecoordocr', doc_id, sequence=sequence)

   


   
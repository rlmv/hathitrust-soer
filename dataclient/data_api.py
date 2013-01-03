

__author__ = 'robertmarchman'

import requests
import json
import xml.etree.ElementTree as ET


from requests_oauthlib import OAuth1
from constants import DATA_BASEURL, SECURE_DATA_BASEURL


class HTDataInterface(object):

    def __init__(self, client_key, client_secret, secure=False):
        """
        Initialize a HTDataInterface object.

        Args:
            client_key: OAuth client client key
            client_secret: secret OAuth key
            secure: toggles http/https session. Defaults to
                 http, use https for access to restricted content.

        """

        self.client_key = client_key
        self.client_secret = client_secret
        self.oauth = OAuth1(client_key=client_key, 
                            client_secret=client_secret, 
                            signature_type='query')

        # initialize persistent Requests session and 
        # attach OAuth credentials to it
        self.rsession = requests.Session()
        self.rsession.auth = self.oauth

        if secure:
            self.baseurl = SECURE_DATA_BASEURL
        else: 
            self.baseurl = DATA_BASEURL


    def _make_request(self, resource, doc_id, sequence=None, 
                        v=1, json=False, callback=None):
        """
        Construct and perform URI request.

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

        # construct optional parameter dictionary
        params = {'v': str(v)}
        if json:
            params['alt'] = 'json'
            if callback:
                params['callback'] = callback

        # perform request and raise errors
        r = self.rsession.get(url, params=params)
        r.raise_for_status()

        return r


    def get_meta(self, doc_id, json=False):
        """
        Retrieve Volume and Rights Metadata resources.

        Args:
            doc_id: document identifier
            json: if json=True, the json representation of
                the resource is returned, otherwise efaults to an atom+xml 
                format.

        Returns: 
            ...

        """
        return self._make_request('meta', doc_id, json=json)


    def get_structure(self, doc_id, json=False):
        """ 
        Retrieve a METS document.

        Args:
            doc_id: target document
            json: toggles json/xml 
        Returns:
            xml or json string

        """
        return self._make_request('structure', doc_id, json=json)


    def get_pagemeta(self, doc_id, seq, json=False):
        """ Retrieve single page metadata. """

        return self._make_request('pagemeta', doc_id, sequence=seq, json=json)


    def get_aggregate(self, doc_id):
        return self._make_request('aggregate', doc_id)

    def get_pageimage(self):
        pass

    def get_pageocr(self):
        pass

    def get_pagecoordocr(self):
        pass



if __name__ == "__main__":

    url = u'https://babel.hathitrust.org/cgi/htd/meta/miun.abr0732.0001.001/2?v=1'

    client_key = u'd4b43a0b2e'
    client_secret= u'f53b0161addebb83d1baf03f7b69'

    # queryoauth = OAuth1(client_key=client_key, client_secret=client_secret, signature_type='query')
    # r = requests.get(turl, auth=queryoauth)

    # print r.text

    diface = HTDataInterface(client_key, client_secret, secure=False)
    # js = diface.make_request(url).json()
    # print json.dumps(js, indent=4)
    # response = diface._make_request('meta', 'miun.abr0732.0001.001', v=1, json=True)
    response = diface.get_aggregate('miun.abr0732.0001.001')

    with open('temp.zip', 'wb') as f:
        f.write(response.content)

    print 'DONE'

  
   


   
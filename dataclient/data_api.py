

__author__ = 'robertmarchman'

import requests
import json

from requests_oauthlib import OAuth1
from constants import DATA_BASEURL, SECURE_DATA_BASEURL


class HTDataInterface(object):

    def __init__(self, client_key, client_secret, secure=False):
        """Initialize a HTDataInterface object.

        :param client_key: OAuth client client key
        :param client_secret: secret OAuth key
        :param secure: toggles http/https session. Defaults to
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


    def make_request(self, url):
        """Process generic URI request."""

        return self.rsession.get(url)
        


    def get_meta(self):
        pass

    def get_structure(self):
        pass

    def get_aggregate(self):
        pass

    def get_pageimage(self):
        pass

    def get_pageocr(self):
        pass

    def get_pagecoordocr(self):
        pass



if __name__ == "__main__":

    url = u'https://babel.hathitrust.org/cgi/htd/meta/miun.abr0732.0001.001'

    client_key = u'd4b43a0b2e'
    client_secret= u'f53b0161addebb83d1baf03f7b69'

    # queryoauth = OAuth1(client_key=client_key, client_secret=client_secret, signature_type='query')
    # r = requests.get(turl, auth=queryoauth)

    # print r.text

    diface = HTDataInterface(client_key, client_secret, secure=False)
    print diface.make_request(url).text
    print diface.make_request(url).url


   
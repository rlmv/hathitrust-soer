import json
import httplib
import urllib
import requests 

OA2_ADDRESS_STUB = "https://silvermaple.pti.indiana.edu:25443/oauth2"
HOST = "https://silvermaple.pti.indiana.edu"
PORT = 25443    

def obtainOAuth2Token(clientID, clientSecret):
    """ function that authorizes with OAuth2 token endpoint, obtains and returns an OAuth2 token
     
    arguments:
    clientID -- client ID or username
    clientSecret -- client secret or password
     
    returns OAuth2 token upon successful authroization.
    raises exception if authorization fails
    """
     
    # forming the OAuth2 token endpoint URL with query string
    oauth2SourceAddress = OA2_ADDRESS_STUB
    params = {"grant_type" : "client_credentials", "client_id" : clientID,  "client_secret" : clientSecret}
    headers = {"content-type" : "application/x-www-form-urlencoded"}
    data = {"null":""}
    r = requests.post(oauth2SourceAddress, params=params, headers=headers, data=data)
    print r.url
    print r.headers
    print r.content
    r.raise_for_status()
    # create an HTTPS connection
    # httpsConn = httplib.HTTPSConnection(OA2_ADDRESS_STUB)
     
    # # make the HTTP request 
    # # request method must be POST
    # # request body must literally say "null"
    # # content-type http header must be "application/x-www-form-urlencoded"
    # httpsConn.request("POST", oauth2SourceAddress, "null", {"content-type" : "application/x-www-form-urlencoded"})
     
    # # get HTTP response back
    # resp = httpsConn.getresponse()
     
    # # make sure the response code is 200, which means OK
    # if (resp.status == 200):
    #     # response body is a JSON string
    #     oauth2JsonStr = resp.read()
    #     # parse JSON string using python built-in json lib
    #     oauth2Json = json.loads(oauth2JsonStr)
         
    #     # remember to close the response and https connection
    #     resp.close()
    #     httpsConn.close()
         
    #     # return the access token
    #     return oauth2Json["access_token"]
     
    # # any other response means the OAuth2 authentication failed. raise exception    
    # else:
    #     status = resp.status
    #     reason = resp.reason
    #     msg = resp.msg
    #     body = resp.read()
    #     resp.close()
    #     httpsConn.close()
    #     raise Exception(str(status) + " " + str(reason) + " " + str(msg) + " " + str(body))


clientID = "d4b43a0b2e"
clientSecret = "f53b0161addebb83d1baf03f7b69"

print obtainOAuth2Token(clientID, clientSecret)


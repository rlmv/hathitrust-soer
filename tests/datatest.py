

# edit oauth_keys.py with your own key
from oauth_keys import client_key, client_secret

if __name__ == "__main__":

    url = u'https://babel.hathitrust.org/cgi/htd/meta/miun.abr0732.0001.001/2?v=1'

    

    # queryoauth = OAuth1(client_key=client_key, client_secret=client_secret, signature_type='query')
    # r = requests.get(turl, auth=queryoauth)

    # print r.text

    diface = HTDataInterface(client_key, client_secret, secure=False)
    # js = diface.make_request(url).json()
    # print json.dumps(js, indent=4)
    # response = diface._make_request('meta', 'miun.abr0732.0001.001', v=1, json=True)
    response = diface.get_structure('mdp.39015000000128')
    print response.url
   

    with open('temp', 'wb') as f:
        f.write(response.content) 

    print 'DONE'

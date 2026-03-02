'''Request .spotify_code'''

import requests
import os
from dotenv import load_dotenv
import random
import webbrowser
import string
from urllib.parse import urlencode

def authorize():
    load_dotenv()
    authurl = 'https://accounts.spotify.com/authorize?'
    cID= os.getenv('cid')
    STATE = ''.join(random.choices(string.ascii_letters,k=16))
    with open(".spotify_state", "w") as f:
        f.write(STATE) 
    scope = 'user-read-private user-read-email user-top-read playlist-read-private'
    REDIRECT_URI = 'http://127.0.0.1:8888/callback'


    params = {"response_type": 'code', "client_id": cID, "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "state": STATE}

    encode_params = urlencode(params)
    main_url = authurl+encode_params
    webbrowser.open(main_url)

authorize()

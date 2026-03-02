'''Request .spotify_code'''
from datetime import datetime, timezone
import requests
import os
from dotenv import load_dotenv
import random
import webbrowser
import string
from urllib.parse import urlencode
import json


CREDS = 'creds.json'

def authorize():
    try:
        print('Try')
        with open(CREDS,'r') as json_file:
            json_data = json.load(json_file)
            print(json_data)
            if 'expire' in json_data:
                expires_at = datetime.fromisoformat(json_data['expire'])
                now = datetime.now(timezone.utc)
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                print(expires_at)
                print(now)
                if now>=expires_at:
                    print("EXPIRED")
                    raise(FileNotFoundError)
    except FileNotFoundError:
        print('File Not Found')
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


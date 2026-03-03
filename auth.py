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
        with open(CREDS,'r') as json_file:
            json_data = json.load(json_file)
            if 'code_expire' in json_data:
                code_expires_at = datetime.fromisoformat(json_data['code_expire'])
                now = datetime.now(timezone.utc)
                if code_expires_at.tzinfo is None:
                    code_expires_at = code_expires_at.replace(tzinfo=timezone.utc)
                if now>=code_expires_at:
                    raise FileNotFoundError
    # except FileNotFoundError:
    except:
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


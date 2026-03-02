'''Gets Access token using Spotify Code'''
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()

url = 'https://accounts.spotify.com/api/token'
ACCESS_FILE = '.spotify_access'

def fetch():
    with open('.spotify_code','r') as f:
        AUTHCODE = f.read().strip()

    params = {
        'grant_type': 'authorization_code',
        'code' : AUTHCODE,
        'redirect_uri' : 'http://127.0.0.1:8888/callback'
    }
    basic = f"{os.getenv('cid')}:{os.getenv('csc')}"
    #basicbytes = basic.encode('utf-8')
    encoded_basic = base64.b64encode(basic.encode()).decode()
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': f'Basic {encoded_basic}'
}

    res = requests.post(url, headers=headers, data=params).json()
    with open(ACCESS_FILE, 'w') as f:
        f.write(res['access_token'])

'''Gets Access token using Spotify Code'''
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta, timezone
import json
import auth
url = 'https://accounts.spotify.com/api/token'
CREDS = 'creds.json'

def fetch():
    try:
        with open(CREDS,'r') as json_file:
            json_data = json.load(json_file)
        EXPIRED=False
        if 'token_expire' in json_data:
            token_expires_at = datetime.fromisoformat(json_data['token_expire'])
            now = datetime.now(timezone.utc)
            if token_expires_at.tzinfo is None:
                token_expires_at = token_expires_at.replace(tzinfo=timezone.utc)
            if now>=token_expires_at:
                EXPIRED=True
        if 'token_expire' not in json_data or EXPIRED:
            if 'code' not in json_data:
                auth.authorize()
            params = {
                'grant_type': 'authorization_code',
                'code' : json_data['code'],
                'redirect_uri' : 'http://127.0.0.1:8888/callback'
                }
            basic = f"{os.getenv('cid')}:{os.getenv('csc')}"
            #basicbytes = basic.encode('utf-8')
            encoded_basic = base64.b64encode(basic.encode()).decode()
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': f'Basic {encoded_basic}'
        }
            res = requests.post(url, headers=headers, data=params).json()
            with open(CREDS, "w") as json_file:
                now_time = datetime.now(timezone.utc) + timedelta(seconds=3600)
                dic = {}
                dic['code'] = res['refresh_token']
                dic['code_expire']= now_time.isoformat()
                dic['token']= res['access_token']
                dic['token_expire']= now_time.isoformat()

                json.dump(dic, json_file, indent=4, sort_keys=True)
        
    # except FileNotFoundError:
    #     auth.authorize()
    except Exception as e:
        print(type(e).__name__, e)

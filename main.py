import callback_server
import auth
import accesstoken
import playlist
import uvicorn
import time
import json

CREDS = 'creds.json'
if __name__=='__main__':
    auth.authorize()
    time.sleep(1)
    accesstoken.fetch()
    with open(CREDS, 'r') as f:
        creds = json.load(f)
        ACCESS_TOKEN = creds['token']
    playlist.get_user_playlist(ACCESS_TOKEN)

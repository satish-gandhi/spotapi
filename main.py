import auth
import callback_server
import accesstoken
import playlist

if __name__=='__main__':
    
    auth.authorize()
    accesstoken.fetch()
    with open('.spotify_access', 'r') as f:
        ACCESS_TOKEN=f.read().strip()
    playlist.get_user_playlist(ACCESS_TOKEN)

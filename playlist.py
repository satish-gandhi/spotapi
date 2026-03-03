import requests
import inquirer

def get_user_playlist(ACCESS_TOKEN):
    GET_PLAYLIST_URL = 'https://api.spotify.com/v1/me/playlists'
    header = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }


    res = requests.get(GET_PLAYLIST_URL, headers=header).json()
    name = show_user_playlist(res['items'])
    choices = [pname for pname in name.keys()]
    playlist_name = [
        inquirer.List(
            'pname',
            message="Which playlist?",
            choices=choices,
        ),
    ]
    pname = inquirer.prompt(playlist_name)
    pid = name[pname['pname']]

def show_user_playlist(res):
    playlist_urlname= {}
    for response in res:
        playlist_urlname[response['name']] = response['id']
    return playlist_urlname


def get_user_tracks(ACCESS_TOKEN):
    playlist = get_user_playlist(ACCESS_TOKEN)

    


    return


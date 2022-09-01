import requests
from os import listdir
from os.path import isfile, join, getmtime
import helper

def load_game_from_microsofts_server(game_id, profile_id):
    url = 'https://aoe.ms/replay/?gameId=' + game_id + '&profileId=' + profile_id

    r = requests.get(url)
    if 'text/plain' in r.headers['content-type'] and r.content.decode() == 'Match not found.':
        return {'error': 'Match not found.'}

    return {'data': r.content}

def check_games_locally(path, filter):
    files = [f for f in listdir(path) if isfile(join(path, f)) and ".aoe2record" in f]
    return files

def sanity_check_path_and_improve_if_needed(path):
    path = path.replace('\\', '/')
    if path[-1] != '/':
        path += '/'
    return path

def guess_playing_time_from_file(path):
    return getmtime(path)
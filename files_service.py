import requests

def load_game_from_aoe2_net(game_id, profile_id):
    url = 'https://aoe.ms/replay/?gameId=' + game_id + '&profileId=' + profile_id

    r = requests.get(url)
    if 'text/plain' in r.headers['content-type'] and r.content.decode() == 'Match not found.':
        return {'error': 'Match not found.'}

    return {'data': r.content}
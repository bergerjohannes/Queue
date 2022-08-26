import requests
import json
import knowledge

def get_additional_meta_info_for_aoe2net(info):
    game_id = info['game_id']
    url = 'https://aoe2.net/api/match?uuid=' + game_id
    r = requests.get(url)
    additional_info = {}
    try:
        additional_info = json.loads(r.content.decode())
    except:
        pass # Can't decode additional info from aoe2.net -> most likely an empty response or an error

    if 'started' in additional_info:
        info['played_at_time'] = int(additional_info['started'])
    if 'leaderboard_id' in additional_info:
        info['ranked_game_type'] = knowledge.get_leaderboard(additional_info['leaderboard_id'])
    else:
        game_with_ai = len({key: value for (key, value) in info['players'].items() if value['type'] == 'AI' }) > 0
        if game_with_ai == True:
            info['ranked_game_type'] = knowledge.get_leaderboard(0) # If AI is present -> unranked
        else:
            info['ranked_game_type'] = 'Unknown'
    if 'players' in additional_info:
        for player in info['players']:
            player_id = info['players'][player]['id']
            additional_player_info = [p for p in additional_info['players'] if p['profile_id'] == player_id][0]
            info['players'][player]['rating'] = additional_player_info['rating']
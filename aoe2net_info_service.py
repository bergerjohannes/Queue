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
        print("Can't decode additional info from aoe2.net.")

    if 'started' in additional_info:
        print(additional_info['started'])
        info['played_at_time'] = int(additional_info['started'])
    if 'started' in additional_info:
        print(additional_info['leaderboard_id'])
        info['ranked_game_type'] = knowledge.get_leaderboard(additional_info['leaderboard_id'])
    else:
        info['ranked_game_type'] = 'Unknown' # ToDo: Add 'Unranked' if AI was included
    if 'players' in additional_info:
        for player in info['players']:
            player_id = info['players'][player]['id']
            additional_player_info = [p for p in additional_info['players'] if p['profile_id'] == player_id][0]
            info['players'][player]['rating'] = additional_player_info['rating']
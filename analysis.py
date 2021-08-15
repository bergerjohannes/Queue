import zipfile
import io
from mgz import header, body, fast
from mgz.summary import Summary

def game_summary(game_id, data):

    game = data['data']
    file_name = 'AgeIIDE_Replay_' + game_id + '.aoe2record'

    players = {}

    with zipfile.ZipFile(io.BytesIO(game)) as zip_ref:
        with zip_ref.open(file_name) as data:
            s = Summary(data)
            players_data = s.get_players()
            for index in range(len(players_data)):
                players[index + 1] = {'name': players_data[index]['name'],
                                      'civilization': players_data[index]['civilization'],
                                      'winner': players_data[index]['winner'],
                                      'user_id': players_data[index]['user_id']}
    
    return players
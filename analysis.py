import zipfile
import io
from mgz import header, body, fast
from mgz.summary import Summary
import ast
import knowledge

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
                                      'civilization_name': knowledge.get_name_for_civ(players_data[index]['civilization']),
                                      'winner': players_data[index]['winner'],
                                      'user_id': players_data[index]['user_id'],
                                      'buildings': {},
                                      'tech': {},
                                      'units': {}}

        with zip_ref.open(file_name) as data:
            header.parse_stream(data)
            fast.meta(data)
            ingame_time = 0
            counter = 0
            while data.tell():
                try:
                    x = fast.operation(data)
                    if x[0].name == 'VIEWLOCK':
                        pass
                    elif x[0].name == 'SYNC':
                        ingame_time += x[1][0]
                    elif x[0].name == 'ACTION':
                        if str(x[1][0]) == 'Action.SPECIAL':
                            pass
                        if str(x[1][0]) == 'Action.RESIGN':
                            player_id = x[1][1]['player_id']
                            players[player_id]['resigned'] = ingame_time
                        if str(x[1][0]) == 'Action.GAME':
                            pass
                        if str(x[1][0]) == 'Action.POSTGAME':
                            pass
                        if str(x[1][0]) == 'Action.DELETE':
                            pass
                        if str(x[1][0]) == 'Action.TRIBUTE':
                            pass
                        if str(x[1][0]) == 'Action.BUILD':
                            player_id = x[1][1]['player_id']
                            building_id = x[1][1]['building_id']
                            players = document_action('buildings', building_id, ingame_time, players, player_id)
                        if str(x[1][0]) == 'Action.DE_QUEUE':
                            player_id = x[1][1]['player_id']
                            unit_id = x[1][1]['unit_id']
                            players = document_action('units', unit_id, ingame_time, players, player_id)
                        if str(x[1][0]) == 'Action.RESEARCH':
                            player_id = x[1][1]['player_id']
                            technology_id = x[1][1]['technology_id']
                            players = document_action('tech', technology_id, ingame_time, players, player_id)
                    elif x[0].name == 'CHAT':
                        dict = ast.literal_eval(x[1].decode('UTF-8'))
                        print(dict['messageAGP'])
                    if x[0].name == 'ACTION':
                        counter += 1
                except EOFError:
                    break

    return players

def document_action(type, event, time, data, player):
    if event in data[player][type]:
        events = data[player][type][event]
        events.append(time)
        data[player][type][event] = events
    else:
        data[player][type][event] = [time]
    return data

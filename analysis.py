from constants import *
from helper import *
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
    info = {}

    with zipfile.ZipFile(io.BytesIO(game)) as zip_ref:
        with zip_ref.open(file_name) as data:
            s = Summary(data)
            players_data = s.get_players()
            info['duration'] = get_readable_time_from_ingame_timestamp(s.get_duration())
            info['map_name'] = s.get_map()['name']
            info['map_size'] = s.get_map()['size']
            info['number_of_players'] = len(players_data)
            teams = []
            for team in s.get_teams():
                team_data = []
                for player in team:
                    team_data.append(player)
                teams.append(team_data)
            info['teams'] = teams
            for index in range(len(players_data)):
                players[index + 1] = {'name': players_data[index]['name'],
                                      CIV: players_data[index][CIV],
                                      'civilization_name': knowledge.get_name_for_civ(players_data[index][CIV]),
                                      'winner': players_data[index]['winner'],
                                      'user_id': players_data[index]['user_id'],
                                      BUILDINGS: {},
                                      RESEARCH: {},
                                      UNITS: {},
                                      AGE_UP_TIMES: [],
                                      DEQUEUE_EVENTS_AT_INITIAL_TC: [],
                                      'number': players_data[index]['number'],
                                      'color': players_data[index]['color_id']
}

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
                            if 'order_type' in x[1][1] and x[1][1]['order_type'] == SPECIAL_ORDER_TYPE_DEQUEUE:
                                for index in range(len(players_data)):
                                    if  INITIAL_TC_ID in players[index+1] and players[index+1][INITIAL_TC_ID] == x[1][1]['object_ids'][0]:
                                        players = document_action(DEQUEUE_EVENTS_AT_INITIAL_TC, None, ingame_time, players, player_id)
                            pass
                        if str(x[1][0]) == 'Action.RESIGN':
                            player_id = x[1][1][PLAYER_ID]
                            players[player_id]['resigned'] = ingame_time
                        if str(x[1][0]) == 'Action.GAME':
                            pass
                        if str(x[1][0]) == 'Action.POSTGAME':
                            pass
                        if str(x[1][0]) == 'Action.DELETE':
                            pass
                        if str(x[1][0]) == 'Action.ORDER':
                            if 'building_id' in x[1][1] and x[1][1]['building_id'] == -1: # This is a dequeue event
                                for index in range(len(players_data)):
                                    if  INITIAL_TC_ID in players[index+1] and 'unit_ids' in x[1][1] and players[index+1][INITIAL_TC_ID] in x[1][1]['unit_ids']:
                                        players = document_action(DEQUEUE_EVENTS_AT_INITIAL_TC, None, ingame_time, players, player_id)
                            pass
                        if str(x[1][0]) == 'Action.GATHER_POINT':
                            pass
                        if str(x[1][0]) == 'Action.BACK_TO_WORK':
                            pass
                        if str(x[1][0]) == 'Action.WORK':
                            pass
                        if str(x[1][0]) == 'Action.CREATE':
                            pass
                        if str(x[1][0]) == 'Action.UNGARRISON':
                            pass
                        if str(x[1][0]) == 'Action.WALL':
                            pass
                        if str(x[1][0]) == 'Action.STANCE':
                            pass
                        if str(x[1][0]) == 'Action.FORMATION':
                            pass
                        if str(x[1][0]) == 'Action.PATROL':
                            pass                      
                        if str(x[1][0]) == 'Action.SELL':
                            pass
                        if str(x[1][0]) == 'Action.BUY':
                            pass
                        if str(x[1][0]) == 'Action.GAME':
                            pass
                        if str(x[1][0]) == 'Action.MOVE':
                            pass
                        if str(x[1][0]) == 'Action.TRIBUTE':
                            pass
                        if str(x[1][0]) == 'Action.REPAIR':
                            pass
                        if str(x[1][0]) == 'Action.ATTACK_GROUND':
                            pass
                        if str(x[1][0]) == 'Action.STOP':
                            pass
                        if str(x[1][0]) == 'Action.GUARD':
                            pass
                        if str(x[1][0]) == 'Action.FOLLOW':
                            pass
                        if str(x[1][0]) == 'Action.DROP_RELIC':
                            pass
                        if str(x[1][0]) == 'Action.FLARE':
                            pass
                        if str(x[1][0]) == 'Action.DE_ATTACK_MOVE':
                            pass
                        if str(x[1][0]) == 'Action.ADD_ATTRIBUTE':
                            pass
                        if str(x[1][0]) == 'Action.GIVE_ATTRIBUTE':
                            pass
                        if str(x[1][0]) == 'Action.AI_ORDER':
                            pass
                        if str(x[1][0]) == 'Action.SPECTATE':
                            pass
                        if str(x[1][0]) == 'Action.ADD_WAYPOINT':
                            pass
                        if str(x[1][0]) == 'Action.SAVE':
                            pass
                        if str(x[1][0]) == 'Action.GROUP_MULTI_WAYPOINTS':
                            pass
                        if str(x[1][0]) == 'Action.CHAPTER':
                            pass
                        if str(x[1][0]) == 'Action.DE_AUTOSCOUT':
                            pass
                        if str(x[1][0]) == 'Action.AI_COMMAND':
                            pass
                        if str(x[1][0]) == 'Action.MAKE':
                            pass
                        if str(x[1][0]) == 'Action.MULTIQUEUE':
                            pass
                        if str(x[1][0]) == 'Action.GATE':
                            pass
                        if str(x[1][0]) == 'Action.QUEUE':
                            pass
                        if str(x[1][0]) == 'Action.TOWN_BELL':
                            pass
                        if str(x[1][0]) == 'Action.BUILD':
                            player_id = x[1][1][PLAYER_ID]
                            building_id = x[1][1][BUILDING_ID]
                            players = document_action(BUILDINGS, building_id, ingame_time, players, player_id)
                        if str(x[1][0]) == 'Action.DE_QUEUE':
                            player_id = x[1][1][PLAYER_ID]
                            unit_id = x[1][1][UNIT_ID]
                            players = document_action(UNITS, unit_id, ingame_time, players, player_id)
                            if unit_id == ID_VILLAGER_MALE and not INITIAL_TC_ID in players[player_id]:
                                players[player_id][INITIAL_TC_ID] = x[1][1]['object_ids'][0]
                        if str(x[1][0]) == 'Action.RESEARCH':
                            player_id = x[1][1][PLAYER_ID]
                            technology_id = x[1][1][TECHNOLOGY_ID]
                            players = document_action(RESEARCH, technology_id, ingame_time, players, player_id)
                        if str(x[1][0]) == 'Action.DE_UNKNOWN_35' or str(x[1][0]) == 'Action.DE_UNKNOWN_37' or str(x[1][0]) == 'Action.DE_UNKNOWN_39' or str(x[1][0]) == 'Action.DE_UNKNOWN_41' or str(x[1][0]) == 'Action.DE_UNKNOWN_109' or str(x[1][0]) == 'Action.DE_UNKNOWN_130' or str(x[1][0]) == 'Action.DE_UNKNOWN_131' or str(x[1][0]) == 'Action.DE_UNKNOWN_135':
                            pass
                    elif x[0].name == 'CHAT':
                        message = ast.literal_eval(x[1].decode('UTF-8'))['messageAGP']
                        for index in range(len(players)):
                            player = players[index + 1]
                            if knowledge.chat_indicates_age_up(message, player['name']):
                                players[index + 1][AGE_UP_TIMES].append(ingame_time)
                    if x[0].name == 'ACTION':
                        counter += 1
                except EOFError:
                    break
    info['players'] = players
    return info

def document_action(type, event, time, data, player):
    if event is None: # This is used for dequeue events where we don't know what was dequeued
        events = data[player][type]
        events.append(time)
        data[player][type] = events
    elif event in data[player][type]:
        events = data[player][type][event]
        events.append(time)
        data[player][type][event] = events
    else:
        data[player][type][event] = [time]
    return data
from constants import *
from helper import *
import zipfile
import io
from mgz import header, body, fast
from mgz.summary import Summary
from mgz.model import parse_match
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
                                      'color': players_data[index]['color_id'],
                                      'apm_over_time': {},
                                      'mean_apm': 0
}
        with zip_ref.open(file_name) as data:
            match = parse_match(data)

            lastActionTime = match.actions[-1].timestamp
            gameDurationMinutes = int(lastActionTime.total_seconds() / 60)
            gameDurationRemainingSeconds = int(lastActionTime.total_seconds() % 60)

            nonRelevantActionsIds = [AI_ORDER, RESIGN, SPECTATE, SAVE, HD_UNKNOWN_34, DE_UNKNOWN_35, DE_UNKNOWN_37, DE_UNKNOWN_39, DE_UNKNOWN_41, DE_UNKNOWN_43, AI_COMMAND, DE_UNKNOWN_80, GAME, DE_UNKNOWN_109, FLARE, DE_UNKNOWN_130, DE_UNKNOWN_131, DE_UNKNOWN_135, DE_UNKNOWN_138, POSTGAME]
            relevantGameActions = list(filter(lambda x: x.type.value not in nonRelevantActionsIds, match.actions))

            actionsPlayer0 = list(
                filter(lambda x: x.player == match.players[0], relevantGameActions))
            actionsPlayer1 = list(
                filter(lambda x: x.player == match.players[1], relevantGameActions))

            apmOverTimePlayer0 = {}
            apmOverTimePlayer1 = {}
            apmMeanPlayer0 = 0
            apmMeanPlayer1 = 0

            for timeframe in range(gameDurationMinutes + 1):
                apmPlayer0InGivenMinute = list(
                    filter(lambda x: x.timestamp.total_seconds() / 60 >= timeframe and x.timestamp.total_seconds() / 60 < timeframe+1, actionsPlayer0))
                apmPlayer1InGivenMinute = list(
                    filter(lambda x: x.timestamp.total_seconds() / 60 >= timeframe and x.timestamp.total_seconds() / 60 < timeframe+1, actionsPlayer1))
                if timeframe == gameDurationMinutes:
                    calculatedAPMForLastMinutePlayer0 = round(
                        len(apmPlayer0InGivenMinute) / gameDurationRemainingSeconds*60)
                    calculatedAPMForLastMinutePlayer1 = round(
                        len(apmPlayer1InGivenMinute) / gameDurationRemainingSeconds*60)

                    apmOverTimePlayer0[timeframe] = calculatedAPMForLastMinutePlayer0
                    apmOverTimePlayer1[timeframe] = calculatedAPMForLastMinutePlayer1
                    apmMeanPlayer0 += calculatedAPMForLastMinutePlayer0
                    apmMeanPlayer1 += calculatedAPMForLastMinutePlayer1
                else:
                    actualAPMForGivenMinutePlayer0 = len(apmPlayer0InGivenMinute)
                    actualAPMForGivenMinutePlayer1 = len(apmPlayer1InGivenMinute)

                    apmOverTimePlayer0[timeframe] = actualAPMForGivenMinutePlayer0
                    apmOverTimePlayer1[timeframe] = actualAPMForGivenMinutePlayer1
                    apmMeanPlayer0 += actualAPMForGivenMinutePlayer0
                    apmMeanPlayer1 += actualAPMForGivenMinutePlayer1

            apmMeanPlayer0 = round(apmMeanPlayer0/(gameDurationMinutes + 1))
            apmMeanPlayer1 = round(apmMeanPlayer1/(gameDurationMinutes + 1))

            players[1]['apm_over_time'] = apmOverTimePlayer0
            players[1]['mean_apm'] = apmMeanPlayer0
            players[2]['apm_over_time'] = apmOverTimePlayer1
            players[2]['mean_apm'] = apmMeanPlayer1

        with zip_ref.open(file_name) as data:
            header.parse_stream(data)
            fast.meta(data)
            ingame_time = 0
            while data.tell():
                try:
                    x = fast.operation(data)
                    if x[0].name == 'VIEWLOCK':
                        pass
                    elif x[0].name == 'SYNC':
                        ingame_time += x[1][0]
                    elif x[0].name == 'START':
                        pass
                    elif x[0].name == 'POSTGAME':
                        pass
                    elif x[0].name == 'SAVE':
                        pass
                    elif x[0].name == 'ACTION': 
                        if str(x[1][0]) == 'Action.SPECIAL':
                            if 'order_type' in x[1][1] and x[1][1]['order_type'] == SPECIAL_ORDER_TYPE_DEQUEUE:
                                for index in range(len(players_data)):
                                    if  INITIAL_TC_ID in players[index+1] and players[index+1][INITIAL_TC_ID] == x[1][1]['object_ids'][0]:
                                        players = document_action(DEQUEUE_EVENTS_AT_INITIAL_TC, None, ingame_time, players, player_id)
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
                        if str(x[1][0]) == 'Action.DE_TRIBUTE':
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
                        if str(x[1][0]) == 'Action.HD_UNKNOWN_34' or str(x[1][0]) == 'Action.DE_UNKNOWN_35' or str(x[1][0]) == 'Action.DE_UNKNOWN_37' or str(x[1][0]) == 'Action.DE_UNKNOWN_39' or str(x[1][0]) == 'Action.DE_UNKNOWN_41' or str(x[1][0]) == 'Action.DE_UNKNOWN_43' or str(x[1][0]) == 'Action.DE_UNKNOWN_80' or str(x[1][0]) == 'Action.DE_UNKNOWN_109' or str(x[1][0]) == 'Action.DE_UNKNOWN_130' or str(x[1][0]) == 'Action.DE_UNKNOWN_131' or str(x[1][0]) == 'Action.DE_UNKNOWN_135' or str(x[1][0]) == 'Action.DE_UNKNOWN_138':
                            pass
                    elif x[0].name == 'CHAT':
                        message = ast.literal_eval(x[1].decode('UTF-8'))['messageAGP']
                        for index in range(len(players)):
                            player = players[index + 1]
                            if knowledge.chat_indicates_age_up(message, player['name']):
                                players[index + 1][AGE_UP_TIMES].append(ingame_time)
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
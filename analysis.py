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
                                      'mean_apm': 0}

        with zip_ref.open(file_name) as data:
            match = parse_match(data)

            lastActionTime = match.actions[-1].timestamp
            gameDurationMinutes = int(lastActionTime.total_seconds() / 60)
            gameDurationRemainingSeconds = int(lastActionTime.total_seconds() % 60)

            nonRelevantActionsIds = [Action.AI_ORDER.name, Action.RESIGN.name, Action.SPECTATE.name, Action.SAVE.name, Action.HD_UNKNOWN_34.name, Action.DE_UNKNOWN_35.name, Action.DE_UNKNOWN_37.name, Action.DE_UNKNOWN_39.name, Action.DE_UNKNOWN_41.name, Action.DE_UNKNOWN_43.name, Action.AI_COMMAND.name, Action.DE_UNKNOWN_80.name, Action.GAME.name, Action.DE_UNKNOWN_109.name, Action.FLARE.name, Action.DE_UNKNOWN_130.name, Action.DE_UNKNOWN_131.name, Action.DE_UNKNOWN_135.name, Action.DE_UNKNOWN_138.name, Action.POSTGAME.name]
            relevantGameActions = list(filter(lambda x: x.type.name not in nonRelevantActionsIds, match.actions))

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
                    operation = x[0].name
                    if operation == Operation.VIEWLOCK:
                        pass
                    elif operation == Operation.SYNC:
                        ingame_time += x[1][0]
                    elif operation == Operation.START:
                        pass
                    elif operation == Operation.POSTGAME:
                        pass
                    elif operation == Operation.SAVE:
                        pass
                    elif operation == Operation.ACTION:
                        action = str(x[1][0])                     
                        if action == Action.SPECIAL:
                            if 'order_type' in x[1][1] and x[1][1]['order_type'] == SPECIAL_ORDER_TYPE_DEQUEUE:
                                for index in range(len(players_data)):
                                    if  INITIAL_TC_ID in players[index+1] and players[index+1][INITIAL_TC_ID] == x[1][1]['object_ids'][0]:
                                        document_action(DEQUEUE_EVENTS_AT_INITIAL_TC, None, ingame_time, players, player_id)
                        if action == Action.RESIGN:
                            player_id = x[1][1][PLAYER_ID]
                            players[player_id]['resigned'] = ingame_time
                        if action == Action.GAME:
                            pass
                        if action == Action.POSTGAME:
                            pass
                        if action == Action.DELETE:
                            pass
                        if action == Action.ORDER:
                            if 'building_id' in x[1][1] and x[1][1]['building_id'] == -1: # This is a dequeue event
                                for index in range(len(players_data)):
                                    if  INITIAL_TC_ID in players[index+1] and 'unit_ids' in x[1][1] and players[index+1][INITIAL_TC_ID] in x[1][1]['unit_ids']:
                                        document_action(DEQUEUE_EVENTS_AT_INITIAL_TC, None, ingame_time, players, player_id)
                            pass
                        if action == Action.GATHER_POINT:
                            pass
                        if action == Action.BACK_TO_WORK:
                            pass
                        if action == Action.WORK:
                            pass
                        if action == Action.CREATE:
                            pass
                        if action == Action.UNGARRISON:
                            pass
                        if action == Action.WALL:
                            pass
                        if action == Action.STANCE:
                            pass
                        if action == Action.FORMATION:
                            pass
                        if action == Action.PATROL:
                            pass                      
                        if action == Action.SELL:
                            pass
                        if action == Action.BUY:
                            pass
                        if action == Action.GAME:
                            pass
                        if action == Action.MOVE:
                            pass
                        if action == Action.TRIBUTE:
                            pass
                        if action == Action.REPAIR:
                            pass
                        if action == Action.ATTACK_GROUND:
                            pass
                        if action == Action.STOP:
                            pass
                        if action == Action.GUARD:
                            pass
                        if action == Action.FOLLOW:
                            pass
                        if action == Action.DROP_RELIC:
                            pass
                        if action == Action.FLARE:
                            pass
                        if action == Action.DE_ATTACK_MOVE:
                            pass
                        if action == Action.ADD_ATTRIBUTE:
                            pass
                        if action == Action.GIVE_ATTRIBUTE:
                            pass
                        if action == Action.AI_ORDER:
                            pass
                        if action == Action.SPECTATE:
                            pass
                        if action == Action.ADD_WAYPOINT:
                            pass
                        if action == Action.SAVE:
                            pass
                        if action == Action.GROUP_MULTI_WAYPOINTS:
                            pass
                        if action == Action.CHAPTER:
                            pass
                        if action == Action.DE_AUTOSCOUT:
                            pass
                        if action == Action.AI_COMMAND:
                            pass
                        if action == Action.MAKE:
                            pass
                        if action == Action.MULTIQUEUE:
                            pass
                        if action == Action.GATE:
                            pass
                        if action == Action.QUEUE:
                            pass
                        if action == Action.TOWN_BELL:
                            pass
                        if action == Action.DE_TRIBUTE:
                            pass
                        if action == Action.BUILD:
                            player_id = x[1][1][PLAYER_ID]
                            building_id = x[1][1][BUILDING_ID]
                            document_action(BUILDINGS, building_id, ingame_time, players, player_id)
                        if action == Action.DE_QUEUE:
                            player_id = x[1][1][PLAYER_ID]
                            unit_id = x[1][1][UNIT_ID]
                            document_action(UNITS, unit_id, ingame_time, players, player_id)
                            if unit_id == ID_VILLAGER_MALE and not INITIAL_TC_ID in players[player_id]:
                                players[player_id][INITIAL_TC_ID] = x[1][1]['object_ids'][0]
                        if action == Action.RESEARCH:
                            player_id = x[1][1][PLAYER_ID]
                            technology_id = x[1][1][TECHNOLOGY_ID]
                            document_action(RESEARCH, technology_id, ingame_time, players, player_id)
                        if action == Action.HD_UNKNOWN_34 or action == Action.DE_UNKNOWN_35 or action == Action.DE_UNKNOWN_37 or action == Action.DE_UNKNOWN_39 or action == Action.DE_UNKNOWN_41 or action == Action.DE_UNKNOWN_43 or action == Action.DE_UNKNOWN_80 or action == Action.DE_UNKNOWN_109 or action == Action.DE_UNKNOWN_130 or action == Action.DE_UNKNOWN_131 or action == Action.DE_UNKNOWN_135 or action == Action.DE_UNKNOWN_138:
                            pass
                    elif operation == Operation.CHAT:
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
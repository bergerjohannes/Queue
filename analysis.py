from constants import *
from helper import *
import zipfile
import io
from mgz import header, fast
from mgz.summary import Summary
import ast
import knowledge

def game_summary(game_id, game):

    game_data = game['data']
    file_name = 'AgeIIDE_Replay_' + game_id + '.aoe2record'

    players = {}
    info = {}

    with zipfile.ZipFile(io.BytesIO(game_data)) as zip_ref:
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
                                      APM_OVER_TIME: {},
                                      MEAN_APM: 0}

        with zip_ref.open(file_name) as data:
            header.parse_stream(data)
            fast.meta(data)
            ingame_time = 0
            while data.tell():
                try:
                    x = fast.operation(data)
                    operation = x[0].name
                    if operation == Operation.SYNC.name:
                        ingame_time += x[1][0]
                    elif operation == Operation.CHAT.name:
                        message = ast.literal_eval(x[1].decode('UTF-8'))[MESSAGE_AGP]
                        for index in range(len(players)):
                            player = players[index + 1]
                            if knowledge.chat_indicates_age_up(message, player['name']):
                                players[index + 1][AGE_UP_TIMES].append(ingame_time)
                    elif operation == Operation.VIEWLOCK.name:
                        pass
                    elif operation == Operation.START.name:
                        pass
                    elif operation == Operation.POSTGAME.name:
                        pass
                    elif operation == Operation.SAVE.name:
                        pass
                    elif operation == Operation.ACTION.name:
                        action = str(x[1][0]).split('.')[1]
                        action_data = x[1][1]

                        # Try to document game effective actions
                        nonRelevantActionsIds = [Action.AI_ORDER.name, Action.RESIGN.name, Action.SPECTATE.name, Action.SAVE.name, Action.HD_UNKNOWN_34.name, Action.DE_UNKNOWN_35.name, Action.DE_UNKNOWN_37.name, Action.DE_UNKNOWN_39.name, Action.DE_UNKNOWN_41.name, Action.DE_UNKNOWN_43.name, Action.AI_COMMAND.name, Action.DE_UNKNOWN_80.name, Action.GAME.name, Action.DE_UNKNOWN_109.name, Action.FLARE.name, Action.DE_UNKNOWN_130.name, Action.DE_UNKNOWN_131.name, Action.DE_UNKNOWN_135.name, Action.DE_UNKNOWN_138.name, Action.POSTGAME.name]
                        if action not in nonRelevantActionsIds:
                            if PLAYER_ID in action_data: # Sadly, not every relevant action has the player id attached to it
                                player_id = action_data[PLAYER_ID]
                                document_apm(ingame_time, players, player_id)

                        if action == Action.SPECIAL.name:
                            if ORDER_TYPE in action_data and action_data[ORDER_TYPE] == SPECIAL_ORDER_TYPE_DEQUEUE:
                                for index in range(len(players_data)):
                                    if  INITIAL_TC_ID in players[index+1] and players[index+1][INITIAL_TC_ID] == action_data[OBJECT_IDS][0]:
                                        document_action(DEQUEUE_EVENTS_AT_INITIAL_TC, None, ingame_time, players, player_id)
                        elif action == Action.RESIGN.name:
                            player_id = action_data[PLAYER_ID]
                            players[player_id][RESIGNED] = ingame_time
                        elif action == Action.GAME.name:
                            pass
                        elif action == Action.POSTGAME.name:
                            pass
                        elif action == Action.DELETE.name:
                            pass
                        elif action == Action.ORDER.name:
                            if BUILDING_ID in action_data and action_data[BUILDING_ID] == -1: # This is a dequeue event
                                for index in range(len(players_data)):
                                    if  INITIAL_TC_ID in players[index+1] and UNIT_IDS in action_data and players[index+1][INITIAL_TC_ID] in action_data[UNIT_IDS]:
                                        document_action(DEQUEUE_EVENTS_AT_INITIAL_TC, None, ingame_time, players, player_id)
                        elif action == Action.GATHER_POINT.name:
                            pass
                        elif action == Action.BACK_TO_WORK.name:
                            pass
                        elif action == Action.WORK.name:
                            pass
                        elif action == Action.CREATE.name:
                            pass
                        elif action == Action.UNGARRISON.name:
                            pass
                        elif action == Action.WALL.name:
                            pass
                        elif action == Action.STANCE.name:
                            pass
                        elif action == Action.FORMATION.name:
                            pass
                        elif action == Action.PATROL.name:
                            pass                      
                        elif action == Action.SELL.name:
                            pass
                        elif action == Action.BUY.name:
                            pass
                        elif action == Action.GAME.name:
                            pass
                        elif action == Action.MOVE.name:
                            pass
                        elif action == Action.TRIBUTE.name:
                            pass
                        elif action == Action.REPAIR.name:
                            pass
                        elif action == Action.ATTACK_GROUND.name:
                            pass
                        elif action == Action.STOP.name:
                            pass
                        elif action == Action.GUARD.name:
                            pass
                        elif action == Action.FOLLOW.name:
                            pass
                        elif action == Action.DROP_RELIC.name:
                            pass
                        elif action == Action.FLARE.name:
                            pass
                        elif action == Action.DE_ATTACK_MOVE.name:
                            pass
                        elif action == Action.ADD_ATTRIBUTE.name:
                            pass
                        elif action == Action.GIVE_ATTRIBUTE.name:
                            pass
                        elif action == Action.AI_ORDER.name:
                            pass
                        elif action == Action.SPECTATE.name:
                            pass
                        elif action == Action.ADD_WAYPOINT.name:
                            pass
                        elif action == Action.SAVE.name:
                            pass
                        elif action == Action.GROUP_MULTI_WAYPOINTS.name:
                            pass
                        elif action == Action.CHAPTER.name:
                            pass
                        elif action == Action.DE_AUTOSCOUT.name:
                            pass
                        elif action == Action.AI_COMMAND.name:
                            pass
                        elif action == Action.MAKE.name:
                            pass
                        elif action == Action.MULTIQUEUE.name:
                            pass
                        elif action == Action.GATE.name:
                            pass
                        elif action == Action.QUEUE.name:
                            pass
                        elif action == Action.TOWN_BELL.name:
                            pass
                        elif action == Action.DE_TRIBUTE.name:
                            pass
                        elif action == Action.BUILD.name:
                            player_id = action_data[PLAYER_ID]
                            building_id = action_data[BUILDING_ID]
                            document_action(BUILDINGS, building_id, ingame_time, players, player_id)
                        elif action == Action.DE_QUEUE.name:
                            player_id = action_data[PLAYER_ID]
                            unit_id = action_data[UNIT_ID]
                            document_action(UNITS, unit_id, ingame_time, players, player_id)
                            if unit_id == ID_VILLAGER_MALE and not INITIAL_TC_ID in players[player_id]:
                                players[player_id][INITIAL_TC_ID] = action_data[OBJECT_IDS][0]
                        elif action == Action.RESEARCH.name:
                            player_id = action_data[PLAYER_ID]
                            technology_id = action_data[TECHNOLOGY_ID]
                            document_action(RESEARCH, technology_id, ingame_time, players, player_id)
                        elif action == Action.HD_UNKNOWN_34.name or action == Action.DE_UNKNOWN_35.name or action == Action.DE_UNKNOWN_37.name or action == Action.DE_UNKNOWN_39.name or action == Action.DE_UNKNOWN_41.name or action == Action.DE_UNKNOWN_43.name or action == Action.DE_UNKNOWN_80.name or action == Action.DE_UNKNOWN_109.name or action == Action.DE_UNKNOWN_130.name or action == Action.DE_UNKNOWN_131.name or action == Action.DE_UNKNOWN_135.name or action == Action.DE_UNKNOWN_138.name:
                            pass
                except EOFError:
                    break

    finalize_apm_calculation(players, ingame_time)

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

def document_apm(ingame_time, data, player):
    current_minute = str(int(ingame_time / 1000 / 60))
    data[player][MEAN_APM] += 1
    if not current_minute in data[player][APM_OVER_TIME]:
        data[player][APM_OVER_TIME][current_minute] = 1
    else:
        data[player][APM_OVER_TIME][current_minute] += 1

def finalize_apm_calculation(players, ingame_time):
    for player in players:
        # Finish mean apm calculation by dividing through the game time 
        players[player][MEAN_APM] = round(players[player][MEAN_APM] / (ingame_time / 1000) * 60)

        # Adapt APM from last minute
        last_minute = str(int(ingame_time / 1000 / 60))
        if last_minute in players[player][APM_OVER_TIME]:
            seconds_in_last_minute = ingame_time / 1000 % 60
            players[player][APM_OVER_TIME][last_minute] = round(players[player][APM_OVER_TIME][last_minute] / seconds_in_last_minute * 60)
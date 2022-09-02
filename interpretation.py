from ctypes import cast
from helper import *
from constants import *
import math
import knowledge
from mgz import header, fast
import ast
import helper

def get_summary_data(summary):
    players = {}
    info = {}
    players_data = summary.get_players()
    info['game_id'] = summary.get_platform()['platform_match_id']
    if summary.get_played() != None:
        info['played_at_time'] = int(summary.get_played())
    info['game_type'] = summary.get_settings()['type'][1]
    info['duration'] = summary.get_duration()
    info['map_name'] = summary.get_map()['name']
    info['map_start_with_palisade_walls'] = summary.get_objects()['palisade_walls']
    info['map_start_with_stone_walls'] = summary.get_objects()['stone_walls']
    tcs_at_start = summary.get_objects()['tcs']
    if tcs_at_start == None:
        info['map_tc_start_type'] = 'Nomad'
    elif tcs_at_start > 1:
        info['map_tc_start_type'] = 'Multiple TCs'
    else:
        info['map_tc_start_type'] = 'Standard'
    info['map_size'] = summary.get_map()['size']
    info['number_of_players'] = len(players_data)
    for index in range(len(players_data)):
        players[index + 1] = {'name': players_data[index]['name'],
                              CIV: players_data[index][CIV],
                              'civilization_name': knowledge.get_name_for_civ(players_data[index][CIV]),
                              'winner': players_data[index]['winner'],
                              'user_id': players_data[index]['user_id'],
                              'human': players_data[index]['human'],
                              BUILDINGS: {},
                              RESEARCH: {},
                              UNITS: {},
                              AGE_UP_TIMES: {},
                              'number': players_data[index]['number'],
                              'color': knowledge.get_color(players_data[index]['color_id']),
                              APM_OVER_TIME: {},
                              MEAN_APM: 0}

    team_number = 1
    for team in summary.get_teams():
        for player in team:
            players[player]['team'] = team_number
        team_number += 1

    info['players'] = players
    return info

def analyze_actions(info, data):
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
                message = x[1].decode('UTF-8')
                try:
                    message = ast.literal_eval(message)[MESSAGE_AGP] # Try to get the actual message out of the dictonary
                except SyntaxError:
                    pass # If we don't have additional info such as player, channel, message, tauntNumber, messageAGP -> we get the message directly
                for index in range(len(info['players'])):
                    player = info['players'][index + 1]
                    age_up = knowledge.chat_indicates_age_up(message, player['name'])
                    if age_up is not NO_AGE_UP:
                        info['players'][index + 1][AGE_UP_TIMES][age_up] = ingame_time
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
                nonRelevantActionsIds = [Action.AI_ORDER.name, Action.RESIGN.name, Action.SPECTATE.name, Action.SAVE.name, Action.HD_UNKNOWN_34.name, Action.DE_UNKNOWN_35.name, Action.DE_UNKNOWN_37.name, Action.DE_UNKNOWN_39.name, Action.DE_UNKNOWN_41.name, Action.DE_UNKNOWN_43.name,
                                             Action.AI_COMMAND.name, Action.DE_UNKNOWN_80.name, Action.GAME.name, Action.DE_UNKNOWN_109.name, Action.FLARE.name, Action.DE_UNKNOWN_130.name, Action.DE_UNKNOWN_131.name, Action.DE_UNKNOWN_135.name, Action.DE_UNKNOWN_138.name, Action.POSTGAME.name]
                if action not in nonRelevantActionsIds:
                    if PLAYER_ID in action_data:  # Sadly, not every relevant action has the player id attached to it
                        player_id = action_data[PLAYER_ID]
                        if player_id in info['players']: # Check for human player
                            document_apm(ingame_time,  info['players'], player_id)
                if action == Action.SPECIAL.name:
                    pass
                elif action == Action.RESIGN.name:
                    player_id = action_data[PLAYER_ID]
                    info['players'][player_id][RESIGNED] = ingame_time
                elif action == Action.GAME.name:
                    pass
                elif action == Action.POSTGAME.name:
                    pass
                elif action == Action.DELETE.name:
                    pass
                elif action == Action.ORDER.name:
                    pass
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
                    document_action(BUILDINGS, building_id, ingame_time,  info['players'], player_id)
                elif action == Action.DE_QUEUE.name:
                    player_id = action_data[PLAYER_ID]
                    unit_id = action_data[UNIT_ID]
                    document_action(UNITS, unit_id, ingame_time, info['players'], player_id)
                elif action == Action.RESEARCH.name:
                    player_id = action_data[PLAYER_ID]
                    technology_id = action_data[TECHNOLOGY_ID]
                    document_action(RESEARCH, technology_id, ingame_time,  info['players'], player_id)
                elif action == Action.HD_UNKNOWN_34.name or action == Action.DE_UNKNOWN_35.name or action == Action.DE_UNKNOWN_37.name or action == Action.DE_UNKNOWN_39.name or action == Action.DE_UNKNOWN_41.name or action == Action.DE_UNKNOWN_43.name or action == Action.DE_UNKNOWN_80.name or action == Action.DE_UNKNOWN_109.name or action == Action.DE_UNKNOWN_130.name or action == Action.DE_UNKNOWN_131.name or action == Action.DE_UNKNOWN_135.name or action == Action.DE_UNKNOWN_138.name:
                    pass
        except EOFError:
            break

    finalize_apm_calculation(info['players'], ingame_time)
    return info

def get_times_for_first_and_second_creation_of(type, id, data):
    first = math.inf
    second = math.inf
    if id in data[type]:
        for index in range(len(data[type][id])):
            if index == 0:
                first = data[type][id][0]
            if index == 1:
                second = data[type][id][1]
    return (first, second)

def get_age_up_time_for_age(age_up_times, age):
    new_age_reached_at = math.inf
    if age in age_up_times:
        new_age_reached_at = age_up_times[age]

    return new_age_reached_at


def get_time_for_research_of(id, data):
    # get last time it was researched in case it was cancelled before and clicked again
    # we don't know if it was cancelled though after the last time it was clicked
    last = math.inf
    if id in data[RESEARCH]:
        last = data[RESEARCH][id][len(data[RESEARCH][id]) - 1]
    return last


def get_build_order(players):
    game_analysis = {}

    for player_number in range(1, len(players) + 1):
        player = players[player_number]
        player_name = player['name']
        team = player['team']
        number = player['number']
        color = player['color']
        player_civ_name = player['civilization_name']
        player_civ_id = player[CIV]
        player_id = player['user_id']
        winner = player['winner']
        if winner == None:
            winner = 'false'
        age_up_times = player[AGE_UP_TIMES]
        apm_over_time = player[APM_OVER_TIME]
        mean_apm = player[MEAN_APM]
        human = player['human']
        player_type = 'Human'

        first_house, second_house = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_HOUSE, player)
        first_barracks, second_barracks = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_BARRACKS, player)
        first_stable, second_stable = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_STABLE, player)
        first_range, second_range = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_RANGE, player)
        first_mill = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_MILL, player)[0]
        first_blacksmith = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_BLACKSMITH, player)[0]
        first_market = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_MARKET, player)[0]
        first_castle, second_castle = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_CASTLE, player)
        first_dock = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_DOCK, player)[0]
        second_tc, third_tc = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_TC, player)

        loom_clicked = get_time_for_research_of(ID_LOOM, player)
        double_bit_axe = get_time_for_research_of(ID_DOUBLE_BIT_AXE, player)
        horse_collar = get_time_for_research_of(ID_HORSE_COLLAR, player)
        fletching = get_time_for_research_of(ID_FLETCHING, player)

        feudal_age_clicked = get_time_for_research_of(ID_FEUDAL_AGE, player)
        castle_age_clicked = get_time_for_research_of(ID_CASTLE_AGE, player)
        imperial_age_clicked = get_time_for_research_of(ID_IMPERIAL_AGE, player)

        feudal_reached = get_age_up_time_for_age(age_up_times, FEUDAL)
        castle_reached = get_age_up_time_for_age(age_up_times, CASTLE)
        imperial_reached = get_age_up_time_for_age(age_up_times, IMPERIAL)

        first_militia, second_militia = get_times_for_first_and_second_creation_of(
            UNITS, ID_MILITA, player)
        first_archer, second_archer = get_times_for_first_and_second_creation_of(
            UNITS, ID_ARCHER, player)
        first_skirm, second_skirm = get_times_for_first_and_second_creation_of(
            UNITS, ID_SKIRMISHER, player)
        first_scout, second_scout = get_times_for_first_and_second_creation_of(
            UNITS, ID_SCOUT, player)
        first_knight, second_knight = get_times_for_first_and_second_creation_of(
            UNITS, ID_KNIGHT, player)
        first_eagle, second_eagle = get_times_for_first_and_second_creation_of(
            UNITS, ID_EAGLE, player)
        first_elephant, second_elephant = get_times_for_first_and_second_creation_of(
            UNITS, ID_BATTLE_ELEPHANT, player)
        first_camel, second_camel = get_times_for_first_and_second_creation_of(
            UNITS, ID_CAMEL, player)

        man_at_arms_upgrade = get_time_for_research_of(
            ID_MAN_AT_ARMS_UPGRADE, player)
        first_tower, second_tower = get_times_for_first_and_second_creation_of(
            BUILDINGS, ID_TOWER, player)

        build = ''

# DRUSH
        build = check_for_dark_age_action(first_barracks, second_house, feudal_age_clicked, castle_age_clicked, first_mill, first_militia, man_at_arms_upgrade, player_civ_id, feudal_reached)

# FEUDAL
        action_feudal_age = check_for_feudal_age_action(first_tower, second_tc, feudal_age_clicked, castle_age_clicked, player[CIV], first_stable, first_range, first_market, first_militia, first_scout, first_archer, first_skirm, man_at_arms_upgrade, first_blacksmith, second_barracks, second_eagle)
        if action_feudal_age is not '':
            if build is not '':
                build += ' → ' + action_feudal_age
            else:
                build = action_feudal_age

# CASTLE
        if action_feudal_age is '': # Only check for Castle Age build if we don't have a Feudal Age build
            action_castle_age = check_for_castle_age_action(first_blacksmith, castle_age_clicked, first_stable, first_camel, first_archer, first_knight, first_elephant, first_range, first_market, second_tc, third_tc, first_castle)
            if action_castle_age is not '':
                if build is not '':
                    build += ' → ' + action_castle_age
                else:
                    build = action_castle_age

# IMPERIAL
        if action_feudal_age is '' and action_castle_age is '': # Only check for Imperial Age build if we don't have a Feudal Age or Castle Age build
            action_imperial_age = check_for_imperial_age_action(first_market, castle_age_clicked, first_blacksmith, first_stable, imperial_age_clicked, first_range)
            if action_imperial_age is not '':
                if build is not '':
                    build += ' → ' + action_imperial_age
                else:
                    build = action_imperial_age

        if build == '':
            build = 'Unknown'

        game_analysis[player_number] = {'type': player_type, 'name': player_name, 'team': team, 'id': player_id, 'number': number, 'color': color, 'winner': winner, 'civ': player_civ_name, 'build': build, AGE_UP_TIMES: {}, 'apm_over_time': apm_over_time, 'mean_apm': mean_apm}
        if human == False:
            del game_analysis[player_number]['name']
            del game_analysis[player_number]['id']
            del game_analysis[player_number]['apm_over_time']
            del game_analysis[player_number]['mean_apm']
            game_analysis[player_number]['type'] = 'AI'

        if FEUDAL in age_up_times:
            game_analysis[player_number][AGE_UP_TIMES][FEUDAL] = get_seconds_time_from_ingame_timestamp(age_up_times[FEUDAL])
        if CASTLE in age_up_times:
            game_analysis[player_number][AGE_UP_TIMES][CASTLE] = get_seconds_time_from_ingame_timestamp(age_up_times[CASTLE])
        if IMPERIAL in age_up_times:
            game_analysis[player_number][AGE_UP_TIMES][IMPERIAL] = get_seconds_time_from_ingame_timestamp(age_up_times[IMPERIAL])

    # Make the player ids the keys of the player dictionary
    ai_counter = 1
    for x in range(8):
        if x+1 in game_analysis:
            if 'id' in game_analysis[x+1]:
                game_analysis[game_analysis[x+1]['id']] = game_analysis[x+1]
            else:
                game_analysis[ai_counter] = game_analysis[x+1]
                ai_counter += 1
            del game_analysis[x+1]

    return game_analysis


def get_times_for_first_and_second_creation_of(type, id, data):
    first = math.inf
    second = math.inf
    if id in data[type]:
        for index in range(len(data[type][id])):
            if index == 0:
                first = data[type][id][0]
            if index == 1:
                second = data[type][id][1]
    return (first, second)


def check_for_dark_age_action(first_barracks, second_house, feudal_age_clicked, castle_age_clicked, first_mill, first_militia, man_at_arms_upgrade, civ, feudal_reached):
    build = ''

    if first_barracks < second_house and civ == 35:  # Lithuanians
        build = '3-Minute Drush'
    elif first_barracks < feudal_age_clicked and first_barracks < first_mill and first_militia < feudal_age_clicked:
        build = 'Pre-Mill Drush'
    elif first_barracks < feudal_age_clicked and (first_militia < feudal_age_clicked or (first_militia < feudal_reached and man_at_arms_upgrade > castle_age_clicked)):
        build = 'Drush'

    return build


def check_for_feudal_age_action(first_tower, second_tc, feudal_age_clicked, castle_age_clicked, civ, first_stable, first_range, first_market, first_militia, first_scout, first_archer, first_skirm, man_at_arms_upgrade, first_blacksmith, second_barracks, second_eagle):
    build = ''

    if first_tower < first_range and first_tower < first_stable and first_tower < first_market:
        build += 'Towers'
    elif second_tc < castle_age_clicked and civ == 8:  # Persians TODO: check for Nomad map!
        build += 'Douche'
    elif second_tc < castle_age_clicked and civ == 34 and second_tc > feudal_age_clicked:  # Cumans
        build += 'Feudal Boom'
    elif first_stable < first_range and first_stable < first_market and first_stable < first_blacksmith and first_scout < first_archer and first_scout < man_at_arms_upgrade and first_scout < castle_age_clicked:
        build += 'Scouts'
        if first_range < castle_age_clicked and first_archer < castle_age_clicked and first_archer < first_skirm:
            build += ' → Archers'
        elif first_range < castle_age_clicked and first_skirm < castle_age_clicked and first_skirm < first_archer:
            build += ' → Skrims'
        else:
            build += ''  # ' → Castle Age'
    elif first_range < first_stable and first_range < first_market and first_archer < castle_age_clicked and first_archer < man_at_arms_upgrade:
        build += 'Archers'
    elif first_range < first_stable and first_range < first_market and first_skirm < castle_age_clicked and first_skirm < man_at_arms_upgrade:
        build += 'Skirms'
    elif first_militia < first_archer and first_militia < first_scout and man_at_arms_upgrade < first_archer and man_at_arms_upgrade < first_scout and man_at_arms_upgrade < first_skirm and man_at_arms_upgrade < castle_age_clicked:
        build += 'Men-at-Arms'
        if first_range < first_stable and first_range < first_market and first_archer < castle_age_clicked:
            build += ' → Archers'
        elif first_tower < first_range and first_tower < first_stable and first_tower < first_market:
            build += ' → Towers'
        elif first_range < first_stable and first_range < first_market and first_skirm < castle_age_clicked and first_skirm < first_archer:
            build += ' → Skrims'
    elif second_barracks < castle_age_clicked and second_eagle < first_archer and second_eagle < castle_age_clicked:
        build += 'Eagles'

    return build


def check_for_castle_age_action(first_blacksmith, castle_age_clicked, first_stable, first_camel, first_archer, first_knight, first_elephant, first_range, first_market, second_tc, third_tc, first_castle):
    build = ''

    if first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_camel < first_archer and first_camel < first_knight and first_camel < first_elephant:
        build += 'FC → Camels'
    elif first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_elephant < first_archer and first_elephant < first_knight and first_elephant < first_camel:
        build += 'FC → Elephants'
    elif first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_knight < first_archer and first_knight < first_elephant and first_knight < first_camel:
        build += 'FC → Knights'
    elif first_blacksmith < castle_age_clicked and first_range < castle_age_clicked and first_archer < first_knight and first_archer > castle_age_clicked:
        build += 'FC → Crossbows'
    elif first_market < castle_age_clicked and first_blacksmith < castle_age_clicked and first_stable > castle_age_clicked and first_range > castle_age_clicked:
        build += 'FC'
        if first_castle < second_tc:
            build += ' → Unique Unit'
        if second_tc < first_knight and second_tc < first_archer and third_tc < first_knight and third_tc < first_archer:
            build += ' → Boom'

    return build


def check_for_imperial_age_action(first_market, castle_age_clicked, first_blacksmith, first_stable, imperial_age_clicked, first_range):
    build = ''

    if first_market < castle_age_clicked and first_blacksmith < castle_age_clicked and first_stable > imperial_age_clicked and first_range > imperial_age_clicked:
        build += 'Fast Imperial'

    return build


def document_action(type, event, time, data, player):
    if event in data[player][type]:
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
        players[player][MEAN_APM] = round(
            players[player][MEAN_APM] / (ingame_time / 1000) * 60)

        # Adapt APM from last minute
        last_minute = str(int(ingame_time / 1000 / 60))
        if last_minute in players[player][APM_OVER_TIME]:
            seconds_in_last_minute = ingame_time / 1000 % 60
            players[player][APM_OVER_TIME][last_minute] = round(
                players[player][APM_OVER_TIME][last_minute] / seconds_in_last_minute * 60)
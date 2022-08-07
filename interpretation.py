from ctypes import cast
from helper import *
from constants import *
import math

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
        number = player['number']
        color = player['color']
        player_civ_name = player['civilization_name']
        player_civ_id = player[CIV]
        player_id = player['user_id']
        winner = player['winner']
        age_up_times = player[AGE_UP_TIMES]
        apm_over_time = player[APM_OVER_TIME]
        mean_apm = player[MEAN_APM]

        first_house, second_house = get_times_for_first_and_second_creation_of(BUILDINGS, ID_HOUSE, player)
        first_barracks, second_barracks = get_times_for_first_and_second_creation_of(BUILDINGS, ID_BARRACKS, player)
        first_stable, second_stable = get_times_for_first_and_second_creation_of(BUILDINGS, ID_STABLE, player)
        first_range, second_range = get_times_for_first_and_second_creation_of(BUILDINGS, ID_RANGE, player)
        first_mill = get_times_for_first_and_second_creation_of(BUILDINGS, ID_MILL, player)[0]
        first_blacksmith = get_times_for_first_and_second_creation_of(BUILDINGS, ID_BLACKSMITH, player)[0]
        first_market = get_times_for_first_and_second_creation_of(BUILDINGS, ID_MARKET, player)[0]
        first_castle, second_castle = get_times_for_first_and_second_creation_of(BUILDINGS, ID_CASTLE, player)
        first_dock = get_times_for_first_and_second_creation_of(BUILDINGS, ID_DOCK, player)[0]
        second_tc, third_tc = get_times_for_first_and_second_creation_of(BUILDINGS, ID_TC, player)

        loom_clicked = get_time_for_research_of(ID_LOOM, player)
        double_bit_axe = get_time_for_research_of(ID_DOUBLE_BIT_AXE, player)
        horse_collar = get_time_for_research_of(ID_HORSE_COLLAR, player)
        fletching = get_time_for_research_of(ID_FLETCHING, player)

        feudal_age_clicked = get_time_for_research_of(ID_FEUDAL_AGE, player)
        castle_age_clicked = get_time_for_research_of(ID_CASTLE_AGE, player)
        imperial_age_clicked = get_time_for_research_of(ID_IMPERIAL_AGE, player)

        feudal_reached = math.inf
        if FEUDAL in age_up_times:
            fefeudal_reachedudal = age_up_times[FEUDAL]

        castle_reached = math.inf
        if CASTLE in age_up_times:
            castle_reached = age_up_times[CASTLE]

        imperial_reached = math.inf
        if IMPERIAL in age_up_times:
            imperial_reached = age_up_times[IMPERIAL]

        first_militia, second_militia = get_times_for_first_and_second_creation_of(UNITS, ID_MILITA, player)
        first_archer, second_archer = get_times_for_first_and_second_creation_of(UNITS, ID_ARCHER, player)
        first_skirm, second_skirm = get_times_for_first_and_second_creation_of(UNITS, ID_SKIRMISHER, player)
        first_scout, second_scout = get_times_for_first_and_second_creation_of(UNITS, ID_SCOUT, player)
        first_knight, second_knight = get_times_for_first_and_second_creation_of(UNITS, ID_KNIGHT, player)
        first_eagle, second_eagle = get_times_for_first_and_second_creation_of(UNITS, ID_EAGLE, player)
        first_elephant, second_elephant = get_times_for_first_and_second_creation_of(UNITS, ID_BATTLE_ELEPHANT, player)
        first_camel, second_camel = get_times_for_first_and_second_creation_of(UNITS, ID_CAMEL, player)

        man_at_arms_upgrade = get_time_for_research_of(ID_MAN_AT_ARMS_UPGRADE, player)
        first_tower, second_tower = get_times_for_first_and_second_creation_of(BUILDINGS, ID_TOWER, player)

        build = ''

# DRUSH
        build = check_for_dark_age_action(first_barracks, second_house, feudal_age_clicked, castle_age_clicked, first_mill, first_militia, man_at_arms_upgrade, player_civ_id, age_up_times)

# FEUDAL
        action_feudal_age = check_for_feudal_age_action(first_tower, second_tc, castle_age_clicked, player[CIV], first_stable, first_range, first_market, first_militia, first_scout, first_archer,first_skirm, man_at_arms_upgrade, first_blacksmith, second_barracks, second_eagle)
        if action_feudal_age is not '':
            if build is not '':
                build += ' → ' + action_feudal_age
            else:
                build = action_feudal_age

# CASTLE
        action_castle_age = check_for_castle_age_action(first_blacksmith, castle_age_clicked, first_stable, first_camel, first_archer, first_knight, first_elephant, first_range, first_market, second_tc, third_tc, first_castle)
        if action_castle_age is not '':
            if build is not '':
                build += ' → ' + action_castle_age
            else:
                build = action_castle_age

# IMPERIAL
        action_imperial_age = check_for_imperial_age_action(first_market, castle_age_clicked, first_blacksmith, first_stable, imperial_age_clicked, first_range)
        if action_imperial_age is not '':
            if build is not '':
                build += ' → ' + action_imperial_age
            else:
                build = action_imperial_age


        game_analysis[player_number] = {'name': player_name, 'id': player_id, 'number': number, 'color': color, 'winner': winner, 'civ': player_civ_name,
                    'build': build, AGE_UP_TIMES: {}, 'apm_over_time': apm_over_time, 'mean_apm': mean_apm}

        if FEUDAL in age_up_times:
            game_analysis[player_number][AGE_UP_TIMES][FEUDAL] = get_readable_time_from_ingame_timestamp(age_up_times[FEUDAL])
        if CASTLE in age_up_times:
            game_analysis[player_number][AGE_UP_TIMES][CASTLE] = get_readable_time_from_ingame_timestamp(age_up_times[CASTLE])
        if IMPERIAL in age_up_times:
            game_analysis[player_number][AGE_UP_TIMES][IMPERIAL] = get_readable_time_from_ingame_timestamp(age_up_times[IMPERIAL])

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

def check_for_feudal_age_action(first_tower, second_tc, castle_age_clicked, civ, first_stable, first_range, first_market, first_militia, first_scout, first_archer,first_skirm, man_at_arms_upgrade, first_blacksmith, second_barracks, second_eagle):
    build = ''

    if first_tower < first_range and first_tower < first_stable and first_tower < first_market:
        build += 'Towers'
    elif second_tc < castle_age_clicked and civ == 8: # Persians
        build += 'Douche'
    elif second_tc < castle_age_clicked and civ == 34: # Cumans
        build += 'Feudal Boom'
    elif first_stable < first_range and first_stable < first_market and first_stable < first_blacksmith and first_scout < first_archer and first_scout < man_at_arms_upgrade and first_scout < castle_age_clicked:
        build += 'Scouts'
        if first_range < castle_age_clicked and first_archer < castle_age_clicked and first_archer < first_skirm:
            build += ' → Archers'
        elif first_range < castle_age_clicked and first_skirm < castle_age_clicked and first_skirm < first_archer:
            build += ' → Skrims'
        else:
            build += '' # ' → Castle Age'
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
        build += 'Fast Camels'
    elif first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_elephant < first_archer and first_elephant < first_knight and first_elephant < first_camel:
        build += 'Fast Elephants'
    elif first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_knight < first_archer and first_knight < first_elephant and first_knight < first_camel:
        build += 'Fast Knights'
    elif first_blacksmith < castle_age_clicked and first_range < castle_age_clicked and first_archer < first_knight and first_archer > castle_age_clicked:
        build += 'Fast Crossbows'
    elif first_market < castle_age_clicked and first_blacksmith < castle_age_clicked and first_stable > castle_age_clicked and first_range > castle_age_clicked:
        build += 'Fast Castle'
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
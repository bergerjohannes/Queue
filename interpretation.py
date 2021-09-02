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
        player_civ = player['civilization_name']
        player_id = player['user_id']
        winner = player['winner']
        age_up_times = player[AGE_UP_TIMES]

        first_house, second_house = get_times_for_first_and_second_creation_of(BUILDINGS, ID_HOUSE, player)
        first_barracks, second_barracks = get_times_for_first_and_second_creation_of(BUILDINGS, ID_BARRACKS, player)
        first_stable, second_stable = get_times_for_first_and_second_creation_of(BUILDINGS, ID_STABLE, player)
        first_range, second_range = get_times_for_first_and_second_creation_of(BUILDINGS, ID_RANGE, player)
        first_mill = get_times_for_first_and_second_creation_of(BUILDINGS, ID_MILL, player)[0]
        first_blacksmith = get_times_for_first_and_second_creation_of(BUILDINGS, ID_BLACKSMITH, player)[0]
        first_market = get_times_for_first_and_second_creation_of(BUILDINGS, ID_MARKET, player)[0]
        first_castle, second_castle = get_times_for_first_and_second_creation_of(BUILDINGS, ID_CASTLE, player)
        first_dock = get_times_for_first_and_second_creation_of(BUILDINGS, ID_DOUBLE_BIT_AXE, player)[0]
        second_tc, third_tc = get_times_for_first_and_second_creation_of(BUILDINGS, ID_TC, player)

        loom_clicked = get_time_for_research_of(ID_LOOM, player)
        double_bit_axe = get_time_for_research_of(ID_DOUBLE_BIT_AXE, player)
        horse_collar = get_time_for_research_of(ID_HORSE_COLLAR, player)

        feudal_age_clicked = get_time_for_research_of(ID_FEUDAL_AGE, player)
        castle_age_clicked = get_time_for_research_of(ID_CASTLE_AGE, player)
        imperial_age_clicked = get_time_for_research_of(ID_IMPERIAL_AGE, player)

        first_militia, second_militia = get_times_for_first_and_second_creation_of(UNITS, ID_MILITA, player)
        first_archer, second_archer = get_times_for_first_and_second_creation_of(UNITS, ID_ARCHER, player)
        first_skrim, second_skirm = get_times_for_first_and_second_creation_of(UNITS, ID_SKIRMISHER, player)
        first_scout, second_scout = get_times_for_first_and_second_creation_of(UNITS, ID_SCOUT, player)
        first_knight, second_knight = get_times_for_first_and_second_creation_of(UNITS, ID_KNIGHT, player)
        first_eagle, second_eagle = get_times_for_first_and_second_creation_of(UNITS, ID_EAGLE, player)
        first_elephant, second_elephant = get_times_for_first_and_second_creation_of(UNITS, ID_BATTLE_ELEPHANT, player)
        first_camel, second_camel = get_times_for_first_and_second_creation_of(UNITS, ID_CAMEL, player)

        man_at_arms_upgrade = get_time_for_research_of(ID_MAN_AT_ARMS_UPGRADE, player)
        first_tower, second_tower = get_times_for_first_and_second_creation_of(BUILDINGS, ID_TOWER, player)

        build = ''

        if first_barracks < second_house and player[CIV] != 17 and player[CIV] == 35:  # Huns & Lithuanians
            build = '3-Minute Drush → '
        elif first_barracks < feudal_age_clicked and first_barracks < first_mill and first_militia < feudal_age_clicked:
            build = 'Pre-Mill Drush → '
        elif 'feudal' in player:
            if first_barracks < feudal_age_clicked and (first_militia < feudal_age_clicked or (
                    first_militia < player['feudal'] and man_at_arms_upgrade > castle_age_clicked)):
                build = 'Drush → '
        elif first_barracks < feudal_age_clicked and first_militia < feudal_age_clicked:
            build = 'Drush'
        if first_tower < first_barracks:
            build += 'Towers'
        elif second_tc < castle_age_clicked and player[CIV] == 8: # Persians
            build += 'Douche'
        elif second_tc < castle_age_clicked and player[CIV] == 34: # Cumans
            build += 'Feudal Boom'
        elif first_stable < first_range and first_stable < first_market and first_scout < first_archer and first_scout < man_at_arms_upgrade and first_scout < castle_age_clicked:
            build += 'Scouts'
        elif first_range < first_stable and first_range < first_market and first_archer < castle_age_clicked and first_archer < man_at_arms_upgrade and first_archer < castle_age_clicked:
            build += 'Archers'
        elif first_range < first_stable and first_range < first_market and first_skrim < castle_age_clicked and first_skrim < man_at_arms_upgrade and first_skrim < castle_age_clicked:
            build += 'Skirms'
        elif first_militia < first_archer and first_militia < first_scout and man_at_arms_upgrade < first_archer and man_at_arms_upgrade < first_scout:
            build += 'Men-at-Arms'
            if first_range < first_stable and first_range < first_market and first_range < first_blacksmith and first_archer < castle_age_clicked:
                build += ' → Archers'
            elif first_tower < first_range and first_tower < first_stable:
                build += ' → Towers'
            elif first_range < first_stable and first_range < first_market and first_range < first_blacksmith and first_archer < castle_age_clicked and first_skrim < first_archer:
                build += ' → Skrims'
        elif second_barracks < castle_age_clicked and second_eagle < first_archer:
            build += 'Eagles'
        elif first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_camel < first_archer and first_knight < first_archer:
            build += 'Fast Camels'
        elif first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_elephant < first_archer and first_knight < first_archer:
            build += 'Fast Elephants'
        elif first_blacksmith < castle_age_clicked and first_stable < castle_age_clicked and first_knight < first_archer:
            build += 'Knights Rush'
        elif first_blacksmith < castle_age_clicked and first_range < castle_age_clicked and first_archer < first_knight and first_archer > castle_age_clicked:
            build += 'FC + Crossbows'
        elif first_market < castle_age_clicked and first_blacksmith < castle_age_clicked and first_stable > castle_age_clicked and first_range > castle_age_clicked:  # player['castle'] - player['feudal'] < (160000 + 5*25000)
            build += 'Fast Castle'
            if first_castle < second_tc:
                build += ' → Unique Unit'
            if second_tc < first_knight and second_tc < first_archer and third_tc < first_knight and third_tc < first_archer:
                build += ' → Boom'
        elif first_market < castle_age_clicked and first_blacksmith < castle_age_clicked and first_stable > imperial_age_clicked and first_range > imperial_age_clicked:
            build += 'Fast Imperial'

        game_analysis[player_number] = {'name': player_name, 'id': player_id, 'number': number, 'color': color, 'winner': winner, 'civ': player_civ,
                    'build': build, AGE_UP_TIMES: {}}

        if 1 <= len(age_up_times):
            game_analysis[player_number][AGE_UP_TIMES]['feudal'] = get_readable_time_from_ingame_timestamp(age_up_times[0])
        if 2 <= len(age_up_times):
            game_analysis[player_number][AGE_UP_TIMES]['castle'] = get_readable_time_from_ingame_timestamp(age_up_times[1])
        if 3 <= len(age_up_times):
            game_analysis[player_number][AGE_UP_TIMES]['imperial'] = get_readable_time_from_ingame_timestamp(age_up_times[2])

        #calculate_TC_idle_time_in_dark_age(player)

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

def calculate_TC_idle_time_in_dark_age(player): # This is not working (yet) because we don't get all dequeue events and sometimes queues are triggered multiple times even if it's technically not possible because the player has not enough resources to afford the unit multiple times
    feudal_age_reached = player[AGE_UP_TIMES][0] # ToDo: what if game ended before Feudal was reached
    loom_queued = player[RESEARCH][ID_LOOM][len(player[RESEARCH][ID_LOOM])-1] # ToDo: what if game ended before Loom was queued
    feudal_age_queued = player[RESEARCH][ID_FEUDAL_AGE][len(player[RESEARCH][ID_FEUDAL_AGE])-1] # ToDo: what if game ended before Feudal was queued

    villagers = player[UNITS][ID_VILLAGER_MALE]
    villagers_in_dark_age = []
    for index in range(len(villagers)):
        if villagers[index] < feudal_age_queued:
            villagers_in_dark_age.append(villagers[index])
    print(f"{player['name']} queued {len(villagers_in_dark_age)} villagers before clicking up.")

    dequeues_at_initial_TC = player[DEQUEUE_EVENTS_AT_INITIAL_TC]
    dequeues_in_dark_age = []
    for index in range(len(dequeues_at_initial_TC)):
        if dequeues_at_initial_TC[index] < feudal_age_queued:
            dequeues_in_dark_age.append(dequeues_at_initial_TC[index])
    print(f"{player['name']} dequeued {len(dequeues_in_dark_age)} villagers or techs before clicking up.")

    active_TC_time = len(villagers_in_dark_age) * 25000
    if loom_queued < feudal_age_queued:
        print("Loom was researched before clicking up.")
        active_TC_time += 25000
    else:
        print("Loom was not researched before clicking up.")

    feudal_age_research_time = 130000
    idle_TC_time = feudal_age_reached - active_TC_time - feudal_age_research_time
    print(f"Calculated idle TC time: {get_readable_time_from_ingame_timestamp(idle_TC_time)}")
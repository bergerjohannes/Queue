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
    if id in data['tech']:
        last = data['tech'][id][len(data['tech'][id]) - 1]
    return last

def get_build_order(players):
    game_analysis = {}

    for player_number in range(1, len(players) + 1):
        player = players[player_number]
        player_name = player['name']
        player_civ = player['civilization_name']
        player_id = player['user_id']
        winner = player['winner']

        first_house, second_house = get_times_for_first_and_second_creation_of('buildings', 70, player)
        first_barracks, second_barracks = get_times_for_first_and_second_creation_of('buildings', 12, player)
        first_stable, second_stable = get_times_for_first_and_second_creation_of('buildings', 101, player)
        first_range, second_range = get_times_for_first_and_second_creation_of('buildings', 87, player)
        first_mill = get_times_for_first_and_second_creation_of('buildings', 68, player)[0]
        first_blacksmith = get_times_for_first_and_second_creation_of('buildings', 103, player)[0]
        first_market = get_times_for_first_and_second_creation_of('buildings', 84, player)[0]
        first_castle, second_castle = get_times_for_first_and_second_creation_of('buildings', 82, player)
        first_dock = get_times_for_first_and_second_creation_of('buildings', 45, player)[0]
        second_tc, third_tc = get_times_for_first_and_second_creation_of('buildings', 621, player)

        loom_clicked = get_time_for_research_of(22, player)
        double_bit_axe = get_time_for_research_of(202, player)
        horse_collar = get_time_for_research_of(14, player)

        feudal_age_clicked = get_time_for_research_of(101, player)
        castle_age_clicked = get_time_for_research_of(102, player)
        imperial_age_clicked = get_time_for_research_of(103, player)

        first_militia, second_militia = get_times_for_first_and_second_creation_of('units', 74, player)
        first_archer, second_archer = get_times_for_first_and_second_creation_of('units', 4, player)
        first_skrim, second_skirm = get_times_for_first_and_second_creation_of('units', 7, player)
        first_scout, second_scout = get_times_for_first_and_second_creation_of('units', 448, player)
        first_knight, second_knight = get_times_for_first_and_second_creation_of('units', 38, player)
        first_eagle, second_eagle = get_times_for_first_and_second_creation_of('units', 751, player)
        first_elephant, second_elephant = get_times_for_first_and_second_creation_of('units', 1132, player)
        first_camel, second_camel = get_times_for_first_and_second_creation_of('units', 329, player)

        man_at_arms_upgrade = get_time_for_research_of(222, player)
        first_tower, second_tower = get_times_for_first_and_second_creation_of('buildings', 79, player)

        build = ''

        if first_barracks < second_house and player['civilization'] != 17 and player['civilization'] == 35:  # Huns & Lithuanians
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
        elif second_tc < castle_age_clicked and player['civilization'] == 8: # Persians
            build += 'Douche'
        elif second_tc < castle_age_clicked and player['civilization'] == 34: # Cumans
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

        game_analysis[player_number] = {'name': player_name, 'id': player_id, 'winner': winner, 'civilization': player_civ,
                    'build': build}
    
    return game_analysis

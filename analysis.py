from constants import *
from helper import *
import zipfile
import io
from mgz.summary import Summary
import interpretation
import aoe2net_info_service
import files_service

def analyze_game_from_microsofts_server(game_id, game):

    game_data = game['data']
    file_name = 'AgeIIDE_Replay_' + game_id + '.aoe2record'

    print('Start analyzing downloaded game: ' + file_name)

    info = {}

    with zipfile.ZipFile(io.BytesIO(game_data)) as zip_ref:
        with zip_ref.open(file_name) as data:
            s = Summary(data)
            info = interpretation.get_summary_data(s)

        with zip_ref.open(file_name) as data:
            info = interpretation.analyze_actions(info, data)
            interpretation_result = interpretation.get_build_order(info['players'])
            info['players'] = interpretation_result
        
        aoe2net_info_service.get_additional_meta_info_from_aoe2net(info)
        return info

def analyze_game_from_local_path(path):
    print('Start analyzing game at location: ' + path)

    info = {}

    with open(path, 'rb') as data:
        s = Summary(data)
        info = interpretation.get_summary_data(s)

        if 'played_at_time' not in info:
            info['played_at_time'] = int(files_service.guess_playing_time_from_file(path) - info['duration'] / 1000) # /1000 because the duration is in miliseconds

    with open(path, 'rb') as data:
        info = interpretation.analyze_actions(info, data)
        interpretation_result = interpretation.get_build_order(info['players'])
        info['players'] = interpretation_result

    aoe2net_info_service.get_additional_meta_info_from_aoe2net(info)
    return info
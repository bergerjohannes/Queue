from constants import *
from helper import *
import zipfile
import io
from mgz.summary import Summary
import interpretation

def analyze_game_from_microsofts_server(game_id, game):

    game_data = game['data']
    file_name = 'AgeIIDE_Replay_' + game_id + '.aoe2record'

    info = {}

    with zipfile.ZipFile(io.BytesIO(game_data)) as zip_ref:
        with zip_ref.open(file_name) as data:
            s = Summary(data)
            info = interpretation.get_summary_data(s)

        with zip_ref.open(file_name) as data:
            info = interpretation.analyze_actions(info, data)
            interpretation_result = interpretation.get_build_order(info['players'])
            info['players'] = interpretation_result
            return info

def analyze_game_from_local_path(path):

    info = {}

    with open(path, 'rb') as data:
        s = Summary(data)
        info = interpretation.get_summary_data(s)

    with open(path, 'rb') as data:
        info = interpretation.analyze_actions(info, data)
        interpretation_result = interpretation.get_build_order(info['players'])
        info['players'] = interpretation_result
        return info
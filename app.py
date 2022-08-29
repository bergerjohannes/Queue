from flask import Flask, request
from flask_cors import CORS, cross_origin
import files_service
import analysis
import database_service

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])
@cross_origin()
def test():
    return {'status': 'Running'}, 200

@app.route('/analyze', methods = ['GET'])
@cross_origin()
def analyze():
    profile_id = request.args.get('profileId', None)
    game_id = request.args.get('gameId', None)
    if profile_id is None or game_id is None:
        return {'error': 'Missing parameters: profile id and/or game id.'}, 400

    data = files_service.load_game_from_microsofts_server(game_id, profile_id)
    if 'error' in data.keys():
        return {'error': data['error']}, 404

    info = analysis.analyze_game_from_microsofts_server(game_id, data)
    return info, 200

@app.route('/batch-analyze', methods = ['GET'])
@cross_origin()
def batch_analyze():
    path = request.args.get('path', None)
    filter = request.args.get('filter', None)
    if path is None:
        return {'error': 'Missing parameter: path. Please provide a query parameter with the full path to the game files you want to analyze.'}, 400

    path = files_service.sanity_check_path_and_improve_if_needed(path)
    games = files_service.check_games_locally(path, None)

    output = {}
    for game in games:
        full_path = path + game
        info = analysis.analyze_game_from_local_path(full_path)
        database_service.save_game_info_to_db(info)
        output[game] = info

    return output, 200

if __name__ == '__main__':
    # This is used when running locally only.
    app.run(host='127.0.0.1', port=8080, debug=True)
from flask import Flask, request
from flask_cors import CORS, cross_origin

import files_service
import analysis

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])
@cross_origin()
def test():
    return {'status': 'Running'}, 200

@app.route('/analyze', methods = ['GET'])
@cross_origin()
def analyze():
    profile_id = request.args.get('profile_id', None)
    game_id = request.args.get('game_id', None)
    if profile_id is None or game_id is None:
        return {'error': 'Missing parameters: profile id and/or game id.'}, 400

    data = files_service.load_game_from_aoe2_net(game_id, profile_id)
    if 'error' in data.keys():
        return {'error': data['error']}, 404

    players = analysis.game_summary(game_id, data)
    return {'status': players}, 200

if __name__ == '__main__':
    # This is used when running locally only.
    app.run(host='127.0.0.1', port=8080, debug=True)
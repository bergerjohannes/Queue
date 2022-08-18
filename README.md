# Queue
With Queue, you can analyze games from Age of Empires II DE. The API returns a JSON with information about the analyzed game such as map, players, result, age up times, guessed build order, etc.

## Setup
1. Create a new virtual environment called **env** with `python3 -m venv env`
2. Start virtual environment with `source env/bin/activate`
3. Install dependencies by execution `python3 -m pip install -r requirements.txt`
4. Run app with the command `python3 app.py`
5. Access app through `http://127.0.0.1:8080/`

## API
To analyze a game, call the `analyze` endpoint with the query parameters `profileId` and `gameId`.
Games can only be analyzed when they are available through `https://aoe.ms`

## Game parser
https://github.com/happyleavesaoc/aoc-mgz

## License
MIT
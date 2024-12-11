from flask import Flask, request
import tmdb
import giphy
import secrets
import config

cfg = config.Load()

app = Flask(__name__)

tmdb_client = tmdb.Client(cfg.tmbd_token)
giphy_client = giphy.Client(cfg.giphy_api_key)

# in-memory storage for all games
games = {}

# create a new game
@app.route('/game', methods=['POST'])
def game():
    data = request.json
    if data is None:
        return {"error": "no data provided"}, 400

    if "actors" not in data:
        return {"error": "no actors provided"}, 400

    if len(data["actors"]) < 2:
        return {"error": "at least 2 actors required"}, 400

    if "answer" not in data:
        return {"error": "no answer provided"}, 400

    # create a new game id
    game_id = secrets.token_urlsafe(8)


    # store the game data in memory
    games[game_id] = data

    return {"game_id": game_id}

# get a game by id
@app.route('/game/<game_id>', methods=['GET'])
def get_game(game_id):
    print("getting game by id:", game_id)
    if game_id not in games:
        return "Game not found", 404

    return games[game_id]["actors"]

# guess a games answer
@app.route('/game/<game_id>', methods=['POST'])
def guess(game_id):
    data = request.json
    if not isinstance(data, dict):
        return {"error": "Invalid JSON format"}, 400

    print("guessing game answer with data:", data)

    if game_id not in games:
        return {"error": "Game not found"}, 404

    guess = data.get("guess")
    if guess == None:
        return {"error": "no guess provided"}, 400

    guess = guess.lower()
    answer = games[game_id]["answer"].lower()

    if guess == answer:
        return { "result": "correct" }
    else:
        return { "result": "incorrect" }


@app.route('/actors/<actor_id>')
def get_actor(actor_id):
    print("getting actor by id:", actor_id)
    try:
        res = tmdb_client.get_actor(actor_id)
        return res
    except Exception as e:
        print("get_actor error: ", e)
        return {"error": str(e)}, 500

@app.route('/movies/actors/<movie_id>')
def get_actors_by_movie_id(movie_id):
    print("getting actors by movie id:", movie_id)
    try:
        res = tmdb_client.get_actors_by_movie_id(movie_id)
        return res
    except Exception as e:
        print("get_actors_by_movie error: ", e)
        return {"error": str(e)}, 500

@app.route('/movies', methods=['GET'])
def search_movies():
    q = request.args.get('query')
    if not q:
        return "No query string", 400

    print("searching for movie with query:", q)

    try:
        res = tmdb_client.search_movie_by_title(q)
        return res
    except Exception as e:
        print("search_movies error: ", e)
        return {"error": str(e)}, 500

@app.route('/gifs', methods=['GET'])
def search_gifs():
    q = request.args.get('query')
    if not q:
        return "No query string", 400

    limit = request.args.get('limit')
    if not limit:
        limit = 1

    print(f"searching for gif with query: {q} and limit: {limit}")

    try:
        res = giphy_client.gifs_search(q, limit)
        return res
    except Exception as e:
        print("giphy error: ", e)
        return {"error": str(e)}, 500


@app.route("/")
def hello_world():
    return "<p>Hi Ralph!</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

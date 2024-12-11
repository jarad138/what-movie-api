# what-movie-api

## How to run the run the server

First add the TMDB and Giphy api key to the `.env` file
in the root directory of the project.

Then install dependencies and start the server.

```bash
# install dependencies
pip install -r requirements.txt

# start the server
python main.py
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 110-778-531
```

## Sample requests

Using curl but you can use whatever you like.

- search for movies

```bash
curl -H "content-type: application/json" http://127.0.0.1:5000/movies\?query\=terminator

[
  {
    "id": 218,
    "popularity": 105.279,
    "release_date": "1984-10-26",
    "title": "The Terminator"
  },
  {
    "id": 280,
    "popularity": 68.941,
    "release_date": "1991-07-03",
    "title": "Terminator 2: Judgment Day"
  }
...
```

Get the actors in the movie.

```bash
curl -H "content-type: application/json" http://127.0.0.1:5000/movies/actors/218

[
  {
    "character": "Punk",
    "id": 2719,
    "name": "Brian Thompson",
    "popularity": 58.746,
    "profile_path": "https://image.tmdb.org/t/p/w200/qooSjBMA1P85JhBpHlwmmisGroO.jpg"
  },
  {
    "character": "Terminator",
    "id": 1100,
    "name": "Arnold Schwarzenegger",
    "popularity": 38.21,
    "profile_path": "https://image.tmdb.org/t/p/w200/z6IbTtI2FWAVZE6b1V4mqEHjwO6.jpg"
  }
  ...
```

Create the game once the user picks to actors
The actor ids are the ids from the previous request and the answer is the movie title
You will be returned the game_id to play the game from here on.

```bash
curl -H "content-type: application/json" http://127.0.0.1:5000/game -d '{"actors":[ 2719, 1100 ], "answer": "The Terminator"}'
{
  "game_id": "QQCPn7mlW38"
}
```

The browser can then hit provide the game_id to get the actors to play the game.
I'll update this to return urls of the actors giphy's or pictures.

```bash
curl -H "content-type: application/json" http://127.0.0.1:5000/game/QQCPn7mlW38
[
  2719,
  1100
]
```

Then to guess the answer send the following request.

```bash
curl -H "content-type: application/json" http://127.0.0.1:5000/game/QQCPn7mlW38 -d '{"guess":"foo"}'
{
  "result": "incorrect"
}

curl -H "content-type: application/json" http://127.0.0.1:5000/game/QQCPn7mlW38 -d '{"guess":"the terminator"}'
{
  "result": "correct"
}
```

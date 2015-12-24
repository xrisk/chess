from pymongo import MongoClient
from flask import Flask
from flask import request
from flask import json
import chess
import Game

app = Flask(__name__)

db = MongoClient("mongodb://hi:hi@ds035735.mongolab.com:35735/chess")\
    .chess.gems


def _json(d):
    if type(d) == str:
        return _json({"response": d})
    elif "response" in d:
        return json.jsonify(d)
    else:
        d["response"] = "OK"
        return json.jsonify(d)


@app.route('/create/')
def create_game():
    """Initialises a new chess game.

    Returns JSON document, with structure
    ```
    {
        _id: <unique game ID>
    }
    ```
    """
    record = Game.Game()
    db.insert_one(record.props)
    return _json({"_id": record["_id"]})


@app.route('/join/<url>/<color>/')
def join(url, color):
    """Allows a player to join a game previously created by `/create/`

    `url` -- _id returned by _create_
    `color` -- the color which this UA wants to play as

    Returns a JSON document with structure =>
    ```
    {
        _id: <unique game ID>
        key: authentication secret for this UA
    }
    ```
    """
    record = db.find_one({"_id": url})
    if color not in ["w", "b"]:
        return json.jsonify({"response": "Bad input."})
    if not record["joined"][color]:
        db.update_one({"_id": record["_id"]},
                      {"$set": {"joined.{}".format(color): True}})

        return _json({"key": record["secret"][color],
                      "_id": record["_id"]})
    else:
        return _json("This colour is already taken.")


@app.route('/status/<game_id>/')
def get_status(game_id):
        """Retrieves status of a chess game previously created by `/create/`

        `game_id` -- unique game ID as returned by /create/

        Returns a JSON document. For the structure of this document,
        look at the `props` attribute of Game.py.
        """

        record = db.find_one({"_id": game_id})
        if record:
            del record["secret"]
            return _json({"data": record})
        else:
            return _json("Game not found.")


@app.route('/api/move/<game_id>/<secret>/', methods=["POST"])
def make_move(game_id, secret):
    """Makes a move :)

    `game_id` -- unique game ID as returned by /create/
    `secret` -- authentication secret for this UA as returned by /join/

    Requires the following POST variables:

    `fen` -- the FEN string the UA currently has
    `move` -- the move which the UA wants to play, in SAN notation

    Returns a JSON document with following structure =>
    ```
    {
        fen: new FEN string after executing requested move
    }
    ```
    """
    for i in ["fen", "move"]:
        try:
            assert i in request.form
        except AssertionError:
            return _json("Bad input.")

    record = db.find_one({"_id": game_id})
    if record:
        if record["joined"]["w"] and record["joined"]["b"]:
            if request.form["fen"] == record["fen"]:
                if record["secret"][request.form["fen"].split()[1]] == secret:
                    this_game = Game.Game()
                    this_game.props = record
                    if request.form["move"] in this_game.legal_moves():
                        this_game.push_san(request.form["move"])
                        db.delete_one({"_id": game_id})
                        db.insert_one(this_game)
                        return _json("OK. New FEN " + this_game.props["fen"])
                    else:
                        return _json("That is not a valid move.")
                else:
                    return _json("Invalid secret. Or it's not your turn.")
            else:
                return _json("Invalid position, update your FEN.")
        else:
            return _json("Both players have not joined yet.")
    else:
        return _json("That game could not be found.")


@app.route('/listMoves/<url>/')
def get_valid_moves(url):
    """ Returns valid moves in SAN notation, for current position of a game.
        These moves will be accepted by /api/move/`

        `url` -- unique game ID to return moves for

        Returns a JSON document with the following structure =>
        {
            moves: [array of valid moves in SAN notation]
        }
    """
    record = db.find_one({"_id": url})
    if record:
        fen = record["fen"]
        board = chess.Board(fen)
        return _json({"moves": [x.uci() for x in board.legal_moves]})
    else:
        return _json("Game not found.")


if __name__ == '__main__':
    app.run(debug=False)

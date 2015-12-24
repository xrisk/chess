from pymongo import MongoClient
from flask import Flask
from flask import request
from flask import json
import chess
import Game

app = Flask(__name__)

db = MongoClient("mongodb://hi:hi@ds035735.mongolab.com:35735/chess")\
    .chess.gems


@app.route('/')
def index():
    return "Go to /create/ to start a new game."


@app.route('/create/')
def create_game():
    diz_gem = Game.Game()
    db.insert_one(diz_gem.props)
    return json.jsonify({"response": "OK", "_id": diz_gem["_id"]})


@app.route('/join/<url>/<color>/')
def join(url, color):
    record = db.find_one({"_id": url})
    if color not in ["w", "b"]:
        return json.jsonify({"response": "Bad input."})
    if not record["joined"][color]:
        db.update_one({"_id": record["_id"]},
                      {"$set": {"joined.{}".format(color): True}})

        return json.jsonify({"response": "OK",
                             "key": record["secret"][color],
                             "_id": record["_id"]})
    else:
        return json.jsonify({"response": "This colour is already taken."})


@app.route('/status/<gem_id>/')
def get_status(gem_id):
        record = db.find_one({"_id": gem_id})
        if record:
            del record["secret"]
            return json.jsonify({"response": "OK", "data": record})
        else:
            return json.jsonify({"response": "Game not found."})


@app.route('/api/move/<game_id>/<secret>/', methods=["POST"])
def make_move(game_id, secret):
    for i in ["fen", "move"]:
        try:
            assert i in request.form
        except AssertionError:
            return json.jsonify({"response": "Bad input."})

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
                        return "OK. New FEN " + str(this_game.props["fen"])
                    else:
                        return "That is not a valid move."
                else:
                    return "Invalid secret. Or it's not your turn."
            else:
                return "You are referring to an old position, update your FEN."
        else:
            return "Both players have not joined yet."
    else:
        return "That game could not be found."


@app.route('/api/moves/<url>/')
def get_valid_moves(url):
    record = db.find_one({"_id": url})
    if record:
        fen = record["fen"]
        board = chess.Board(fen)
        return json.jsonify({"response": "OK",
                            "moves": [x.uci() for x in board.legal_moves]})
    else:
        return json.jsonify({"response": "Game not found."})


if __name__ == '__main__':
    app.run(debug=True)

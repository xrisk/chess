from pymongo import MongoClient
from flask import Flask
from flask import request
import chess
import Game

app = Flask(__name__)

db = MongoClient("mongodb://hi:hi@ds035735.mongolab.com:35735/chess")\
    .chess.gems


@app.route('/')
def index():
    return "Go to /api/create/ to start a new game."


@app.route('/api/create/')
def create_game():
    diz_gem = Game.Game()
    db.insert_one(diz_gem.props)
    return str(diz_gem.props)


@app.route('/api/fen/<gem_id>/')
def get_fen(gem_id):
    try:
        return str(db.find_one({"_id": str(gem_id)}))
    except Exception, e:
        print e


@app.route('/api/move/<url>/', methods=["POST"])
def make_move(url):
    assert len(url) == 10
    for i in ["fen", "move"]:
        try:
            assert i in request.form
        except AssertionError, e:
            return "Bad form."
    try:
        record = db.find_one({"_id": url[:6]})
        if not record:
            return "Gaem not found."
        if request.form["fen"] == record["fen"]:
            if record["secret"][request.form["fen"].split()[1]] == url[-4:]:
                this_game = Game.Game()
                this_game.props = record
                assert request.form["move"] in this_game.legal_moves()
                this_game.push_san(request.form["move"])
                db.delete_one({"_id": url[:6]})
                db.insert_one(this_game)
                return "OK"
            else:
                return "Invalid secret."
        else:
            return "You are referring to an old position, update your FEN."
    except Exception, e:
        return "Something went wrong, we have no clue what " + str(e)


@app.route('/api/moves/<fen>/')
def get_valid_moves(fen):
    return [x.uci() for x in chess.Board(fen).legal_moves]


if __name__ == '__main__':
    app.run(debug=True)

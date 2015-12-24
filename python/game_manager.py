from pymongo import MongoClient
from flask import Flask
from flask import request
import Game

app = Flask(__name__)

db = MongoClient("mongodb://hi:hi@ds035735.mongolab.com:35735/chess")\
    .chess.gems


@app.route('/')
def index():
    return "THIS IS CHESS !!!11!!"


@app.route('api/create/')
def create_game():
    diz_gem = Game.Game()
    db.insert_one(str(diz_gem))
    return str(diz_gem)


@app.route('/api/fen/<gem_id>/')
def get_fen(gem_id):
    try:
        return str(db.find_one({"url": gem_id}))
    except Exception, e:
        print e


@app.route('/api/move/<url>/', method=["post"])
def make_move(url):
    for i in ["color", "secret", "fen", "move"]:
        assert i in request.form
    assert request.form["color"] in ["black", "white"]
    try:
        record = db.find_one({"url": url})
        if record["secret"][request.form["color"]] == request.form["secret"]:
            game = Game.Game(record)
            assert request.form["move"] in game.moves_here
            game.push_san(request.form["move"])
    except:
        raise


if __name__ == '__main__':
    app.run(debug=True)

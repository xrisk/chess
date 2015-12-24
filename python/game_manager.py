from pymongo import MongoClient
from flask import Flask
import Game

app = Flask(__name__)

db = MongoClient("mongodb://hi:hi@ds035735.mongolab.com:35735/chess")\
    .chess.gems


@app.route('/')
def index():
    return "THIS IS CHESS !!!11!!"


@app.route('/create/')
def create_game():
    diz_gem = Game.Game()
    db.insert_one(diz_gem)
    ret = str(diz_gem["secret"]) + str(diz_gem["url"])
    return ret


@app.route('/<gem_id>')
def get_fen(gem_id):
    try:
        return str(db.find_one({"url": gem_id}))
    except Exception, e:
        print e


if __name__ == '__main__':
    app.run(debug=True)

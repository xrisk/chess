import pymongo
import Game


def create_game(pymongo_instance):
    diz_gem = Game.Game()
    pymongo_instance.insert_one(diz_gem)
    return diz_gem


def get_gaem(pymongo_instance, url):
    try:
        return pymongo_instance.find_one({"url": url})
    except:
        print "THEFUCK"

db = pymongo.MongoClient("mongodb://hi:hi@ds035735.mongolab.com:35735/chess")
create_game(db.chess.gems)

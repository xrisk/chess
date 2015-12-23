import pymongo
import Game


def create_game(pymongo_instance):
    diz_gem = Game.Game()
    record = pymongo_instance.insert_one(diz_gem)
    print record
    diz_id = record.inserted_id
    print diz_id

db = pymongo.MongoClient()
create_game(db.chez.gems)

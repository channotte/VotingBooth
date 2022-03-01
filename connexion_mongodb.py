import datetime
from pymongo import MongoClient
import pprint


def connect_db(server='localhost', port_number=27017):
    conn = MongoClient(server, port_number)
    db = conn.inauguration_test
    collection = db.inauguration
    return collection


def write_db(collection, totalFingers, hand="", hash_val = "NoVote" ):
    record = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "Hash": hash_val,
              "hand": hand,
              "Vote": str(totalFingers)}
    collection.insert_one(record)


collection_inauguration = connect_db()
#write_db(collection_inauguration, totalFingers, hand)
request = [{'$group': {'_id': '$Hash', 'Vote1': {'$sum': {'$cond': [{'$eq': ['$Vote', '1']}, 1, 0]}},
    'Vote2': {'$sum': {'$cond': [{'$eq': ['$Vote', '2']}, 1, 0]}},
    'Vote3': {'$sum': {'$cond': [{'$eq': ['$Vote', '3']}, 1, 0]}},
    'Vote4': {'$sum': {'$cond': [{'$eq': ['$Vote', '4']}, 1, 0]}},
    'Vote5': {'$sum': {'$cond': [{'$eq': ['$Vote', '5']}, 1, 0]}}}}]

pprint.pprint(list(collection_inauguration.aggregate(request)))

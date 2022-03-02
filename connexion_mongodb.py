import datetime, time
from pymongo import MongoClient
import pprint
import pandas as pd



def connect_db(server='localhost', port_number=27017):
    conn = MongoClient(server, port_number)
    db = conn.inauguration_test
    collection = db.inauguration
    return collection


def write_db(collection, totalFingers, hand="", hash_val="NoVote"):
    record = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Hash": hash_val, "hand": hand,
              "Vote": str(totalFingers)}
    collection.insert_one(record)


t_debut = time.time()

collection_inauguration = connect_db()
# write_db(collection_inauguration, totalFingers, hand)
request = [{'$group': {'_id': '$Hash', 'Vote1': {'$sum': {'$cond': [{'$eq': ['$Vote', '1']}, 1, 0]}},
                       'Vote2': {'$sum': {'$cond': [{'$eq': ['$Vote', '2']}, 1, 0]}},
                       'Vote3': {'$sum': {'$cond': [{'$eq': ['$Vote', '3']}, 1, 0]}},
                       'Vote4': {'$sum': {'$cond': [{'$eq': ['$Vote', '4']}, 1, 0]}},
                       'Vote5': {'$sum': {'$cond': [{'$eq': ['$Vote', '5']}, 1, 0]}}}}]

request2 = [{'$group': {'_id': '$Hash', 'Vote1': {'$sum': {'$cond': [{'$eq': ['$Vote', '1']}, 1, 0]}},
                        'Vote2': {'$sum': {'$cond': [{'$eq': ['$Vote', '2']}, 1, 0]}},
                        'Vote3': {'$sum': {'$cond': [{'$eq': ['$Vote', '3']}, 1, 0]}},
                        'Vote4': {'$sum': {'$cond': [{'$eq': ['$Vote', '4']}, 1, 0]}},
                        'Vote5': {'$sum': {'$cond': [{'$eq': ['$Vote', '5']}, 1, 0]}}}},
            {'$addFields': {'Votemax': {'$max': ['$Vote1', '$Vote2', '$Vote3', '$Vote4', '$Vote5']}}},
            {'$addFields': {'VoteValue': {'$cond': [{'$eq': ['$Votemax', '$Vote1']}, 'Vote1', {
                                          '$cond': [{'$eq': ['$Votemax', '$Vote2']}, 'Vote2',
                                        {'$cond': [{'$eq': ['$Votemax', '$Vote3']}, 'Vote3', {
                                          '$cond': [{'$eq': ['$Votemax', '$Vote4']}, 'Vote4',
                                        {'$cond': [{'$eq': ['$Votemax', '$Vote5']}, 'Vote5', 'Vote0']}]}]}]}]}}}]

liste_vote = list(collection_inauguration.aggregate(request2))
# pprint.pprint(liste_vote)

df_vote = pd.DataFrame(liste_vote)
df_votants = df_vote[~df_vote["_id"].str.contains("NoVote")]
df_votants['VoteValue'].value_counts().sort_index()
print(df_vote.head(10))
t_end = time.time()

print("Temps execution", t_end - t_debut)

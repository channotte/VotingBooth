import pandas as pd
import os

header_list = ["date","hashKey","hand","vote"]
# df = pd.read_csv("C:\\VotingBooth\\data.csv",names=header_list)
df = pd.read_csv("data.csv",names=header_list)
results = pd.DataFrame(columns={'title','value'})

# Get total number of records
NombreDeFrames = df.shape[0]
results = results.append({"title":"Nombre total de frames", 'value':NombreDeFrames}, ignore_index=True)

# Get left or right hand numbers
mainGauche = sum((df["hand"]=="Gauche"))
mainDroite = sum((df["hand"]=="Droite"))
results = results.append({"title":"Main gauche", 'value':mainGauche}, ignore_index=True)
results = results.append({"title":"Main droite", 'value':mainDroite}, ignore_index=True)

# Nombre de votes
nombreDeVotes = df["hashKey"].nunique()-1
results = results.append({"title":"Nombre de votes", 'value':nombreDeVotes}, ignore_index=True)

# Taux d'utilisation de la borne
TauxUtilisation = (mainGauche+mainDroite)/NombreDeFrames
results = results.append({"title":"Taux d'utilisation", 'value':TauxUtilisation}, ignore_index=True)

# Votes Par Asso
Vote1 = sum((df["vote"]=="1"))
Vote2 = sum((df["vote"]=="2"))
Vote3 = sum((df["vote"]=="3"))
Vote4 = sum((df["vote"]=="4"))
Vote5 = sum((df["vote"]=="5"))

results = results.append({"title":"Vote1",  'value':Vote1}, ignore_index=True)
results = results.append({"title":"Vote2",  'value':Vote2}, ignore_index=True)
results = results.append({"title":"Vote3",  'value':Vote3}, ignore_index=True)
results = results.append({"title":"Vote4",  'value':Vote4}, ignore_index=True)
results = results.append({"title":"Vote5",  'value':Vote5}, ignore_index=True)

print(results)
# results.to_csv("C:\\VotingBooth\\stats.csv")
results.to_csv("stats.csv")
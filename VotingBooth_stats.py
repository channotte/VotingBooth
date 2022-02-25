import pandas as pd
import os

header_list = ["date","hashKey","hand","vote"]
df = pd.read_csv("C:\\VotingBooth\\data.csv",names=header_list)

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
Asso1 = sum((df["vote"]=="1"))
Asso2 = sum((df["vote"]=="2"))
Asso3 = sum((df["vote"]=="3"))
Asso4 = sum((df["vote"]=="4"))
results = results.append({"title":"Asso1",  'value':Asso1}, ignore_index=True)
results = results.append({"title":"Asso2",  'value':Asso2}, ignore_index=True)
results = results.append({"title":"Asso3",  'value':Asso3}, ignore_index=True)
results = results.append({"title":"Asso4",  'value':Asso4}, ignore_index=True)
print(results)
results.to_csv("C:\\VotingBooth\\stats.csv")
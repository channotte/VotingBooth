import datetime, time
from pymongo import MongoClient
import pandas as pd
# import matplotlib
# matplotlib.use("Qt5Agg")
# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
from PIL import Image
import io

pd.options.plotting.backend = "plotly"
import plotly
import plotly.express as px
import base64


def connect_db(server='localhost', port_number=27017):
    conn = MongoClient(server, port_number)
    db = conn.inauguration_test
    collection = db.inauguration
    return collection


def write_db(collection, totalFingers, hand="", hash_val="NoVote"):
    if totalFingers == 'None':
        totalFingers = '0'

    record = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "Hash": hash_val,
              "hand": hand,
              "Vote": str(totalFingers)}
    collection.insert_one(record)


def make_request(collection, request):
    liste_vote = []

    try:
        liste_vote = list(collection.aggregate(request))
    finally:
        df_vote = pd.DataFrame(liste_vote)

    return df_vote


def retrieve_votants(df_vote):
    df_counts = []
    try:
        df_votants = df_vote[~df_vote["_id"].str.contains("NoVote")]
        df_counts = df_votants['VoteValue'].value_counts().sort_index()
    finally:
        return df_counts


# def draw_pie(dataframe, filename, other):
#     fig = px.pie(dataframe, values='tip', names='day')
#
#     ax = dataframe.plot.pie(y=0, colormap='Pastel1', autopct='%.0f%%', ylabel=' ', title=str(other))
#     ax.figure.savefig(filename, format='png')
#     # return ax


def draw_pie_plotly(dataframe, filename, title, engine="kaleido"):
    fig = px.pie(dataframe, values='valeur', names=dataframe.index, title=str(title),
                 color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.3)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#f7f7f7")
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color="#f7f7f7", width=3)),
                      textfont_size=19)
    fig.update_layout(title=dict(yanchor="bottom", y=0.95, xanchor="center", x=0.5))
    fig.update_layout(margin=dict(l=20, r=20, b=5, t=40, pad=0), title_font_size=25)

    fig.write_image(filename, format='png', engine=engine)


def draw_horizontal_bar_plotly(dataframe, filename, title, engine="kaleido"):
    fig = px.bar(dataframe, x="vote", y="stack", title=str(title), text_auto=True, barmode='relative',
                 orientation="h", labels={},
                 color="Valeurs", color_discrete_sequence=px.colors.qualitative.Pastel, height=220, width=1400)
    fig.update_yaxes(visible=False)
    fig.update_layout(xaxis={"ticksuffix": "%"}, xaxis_title=None)
    fig.update_xaxes(tickformat='.1f')
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
                      uniformtext_minsize=10, uniformtext_mode='hide')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#f7f7f7",
                      barnorm="percent")
    fig.update_traces(textposition='inside', marker=dict(line=dict(color="#f7f7f7", width=2)), textfont_size=20)
    fig.update_layout(xaxis_title=None, legend_font_size=25, title_font_size=25, legend_title="")
    fig.write_image(filename, format='png', engine=engine)


def encode_image(filename):
    im = Image.open(filename)
    data = io.BytesIO()
    im.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data


def main():
    t_debut = time.time()
    totalFingers = "5"
    hand = "Droite"
    collection_inauguration = connect_db()
    write_db(collection_inauguration, totalFingers, hand)

    request = [{'$group': {'_id': '$Hash', 'Vote1': {'$sum': {'$cond': [{'$eq': ['$Vote', '1']}, 1, 0]}},
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

    df_vote = make_request(collection_inauguration, request)
    df_votants = retrieve_votants(df_vote)
    collection_inauguration.count()
    print(df_votants.head(10))
    t_end = time.time()

    print("Temps execution", t_end - t_debut)


if __name__ == "__main__":
    main()

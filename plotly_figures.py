import pandas as pd

pd.options.plotting.backend = "plotly"
import plotly
import plotly.express as px
import base64
from PIL import Image
import io


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


def draw_bar_hands(dataframe, filename, title, engine="kaleido"):
    try:
        fig = px.bar(dataframe, x="vote", y="stack", title=title, text_auto=True, barmode='relative',
                     orientation="h", labels={},
                     color="Valeurs", color_discrete_sequence=px.colors.qualitative.Pastel, height=220, width=1000)
        # fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(xaxis={"ticksuffix": "%"})
        fig.update_xaxes(tickformat='.1f')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
                          uniformtext_minsize=10, uniformtext_mode='hide')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#f7f7f7",
                          barnorm="percent")
        fig.update_traces(textposition='inside', marker=dict(line=dict(color="#f7f7f7", width=2)), textfont_size=20)
        fig.update_layout(xaxis_title=None, legend_font_size=20, title_font_size=25, legend_title="")

        fig.write_image(filename, format='png', engine="orca")
    except Exception as e:
        print(e)
        pass


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


def draw_horizontal_bar_plotly_opt2(dataframe, filename, title, engine="kaleido"):
    try:
        fig = px.bar(dataframe, x="Valeurs", y="vote", title=title, text_auto=True, barmode='relative', labels={},
                     color="Valeurs", color_discrete_sequence=px.colors.qualitative.Pastel, height=500, width=1000)
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
                          uniformtext_minsize=10, uniformtext_mode='hide', font_color="#f7f7f7")
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', bargap=0.5)
        fig.update_traces(textposition='inside', marker=dict(line=dict(color="#f7f7f7", width=3)), textfont_size=20)
        fig.update_layout(xaxis_title=None, yaxis_title="Nombre de votes", legend_font_size=17, title_font_size=25,
                          legend_title="")

        fig.write_image(filename, format='png', engine="orca")
    except Exception as e:
        print(e)
        pass


def encode_image(filename):

    im = Image.open(filename)
    data = io.BytesIO()
    im.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data


def main():
    data = {"vote": [255, 345, 563, 481, 100],
            "Valeurs": ['Authenticité', "Ouverture", "Elégance", "Engagement", "Courage"]}
    data_main = {"vote": [255, 345], "Valeurs": ['Main Gauche', "Main Droite"], 'stack': [0, 0]}

    draw_horizontal_bar_plotly_opt2(pd.DataFrame(data), filename='static/repartition.png',
                                    title="Répartition des votes")
    encoded_repartition = encode_image('static/repartition.png')
    print(encoded_repartition)

    draw_bar_hands(pd.DataFrame(data_main), filename='static/barhands.png', title="Main utilisée pour le vote")
    encoded_img_data = encode_image("static/barhands.png")
    print(encoded_img_data)


if __name__ == "__main__":
    main()

# import cv2
# cap = cv2.VideoCapture()
# # The device number might be 0 or 1 depending on the device and the webcam
# cap.open(0, cv2.CAP_DSHOW)
# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
import plotly.io as pio
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"
scope = pio.kaleido.scope
#
# data_main = {"vote": [250, 300], "Valeurs": ['Main Gauche', "Main Droite"], 'stack': [0, 0]}
# dataframe = pd.DataFrame(data_main)
# title = "Bonjour"
filename = "Bonjour.png"


fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with fig.show()"
)
# fig.show()
# fig = px.bar(dataframe, x="vote", y="stack", title=title, text_auto=True, barmode='relative',
#                  orientation="h", labels={},
#                  color="Valeurs", color_discrete_sequence=px.colors.qualitative.Pastel, height=220, width=1000)
# # fig.update_xaxes(visible=False)
# fig.update_yaxes(visible=False)
# fig.update_layout(xaxis={"ticksuffix": "%"})
# fig.update_xaxes(tickformat='.1f')
# fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
#                   uniformtext_minsize=10, uniformtext_mode='hide')
# fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#f7f7f7",
#                   barnorm="percent")
# fig.update_traces(textposition='inside', marker=dict(line=dict(color="#f7f7f7", width=2)), textfont_size=20)
# fig.update_layout(xaxis_title=None, legend_font_size=20, title_font_size=25, legend_title="")

fig.write_image(filename, format='png', engine="orca")

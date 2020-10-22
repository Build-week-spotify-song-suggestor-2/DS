import os
import pickle
import pandas

import plotly.graph_objects as go
import chart_studio.plotly as py
from chart_studio.tools import set_credentials_file
from dotenv import load_dotenv
load_dotenv()

PLOTLY_USERNAME = os.getenv("PLOTLY_USERNAME")
PLOTLY_API_KEY = os.getenv("PLOTLY_API_KEY")

chart_id = 0

set_credentials_file(
    username=PLOTLY_USERNAME,
    api_key=PLOTLY_API_KEY
)

basedir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(basedir, '../../ml_model/recommendation_model.sav')
df_path = os.path.join(basedir, '../../ml_model/song_dataset.pkl')

with open(model_path, 'rb') as f:
  model = pickle.load(f)

with open(df_path, 'rb') as f:
  df = pickle.load(f)


def find_recommended_songs(track_id):
    song_index = df.index[df['id'] == track_id]
    audio_features = df.iloc[song_index, 3:].to_numpy()
    indices = model.kneighbors(audio_features)[1]
    return df.loc[indices[0], 'id'].tolist()


def track_id_in_df(track_id):
  return len(df.index[df['id'] == track_id]) > 0


def get_radar_plot(track_ids):
    """
      Create combined radar plots of the recommended songs for the given track id.
    """
    global chart_id
    songs = [df[df["id"] == id] for id in track_ids]

    fig = go.Figure()
    audio_features = ["acousticness", "danceability", "energy", 
                      "liveness",  "speechiness",  "valence"]

    for song in songs:
      fig.add_trace(go.Scatterpolar(
        r=[float(song[feature]) for feature in audio_features],
        theta=audio_features,
        fill="toself",
        name="Product A",
        opacity=0.9
      ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 0.7]
        )),
      showlegend=False,
      title = "10 recommended songs from AutoEncoder - Neural Network Model"
    )


    chart = py.plot(
        fig,
        filename=f"track_id_{chart_id}",
        auto_open=False,
        fileopt='overwrite',
        sharing='public'
    )
    
    chart_id += 1

    return chart
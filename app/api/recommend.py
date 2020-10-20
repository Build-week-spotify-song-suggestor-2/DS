import os
import pickle
import pandas

basedir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(basedir, '../../ml_model/recommendation_model.sav')
df_path = os.path.join(basedir, '../../ml_model/song_dataset.pkl')

with open(model_path, 'rb') as f:
  model = pickle.load(f)

with open(df_path, 'rb') as f:
  df = pickle.load(f)


def find_recommended_songs(track_id):
    # from track_id to audio_features
    song_index = df.index[df['id'] == track_id]
    audio_features = df.iloc[song_index, 3:].to_numpy()
    # recommendation model
    distances, indices = model.kneighbors(audio_features) #.reshape(1, -1)
    return df.loc[indices[0], 'id'].tolist()
  
    # how to search song names from ids
    # on the ML side
    # recommended_song_list = []
    # for recommend in recommended_list:
    #     recommend_song_name=df[df['id']==recommend]
    #     recommended_song_list.append(recommend_song_name)
    # return recommended_song_list

def track_id_in_df(track_id):
  return len(df.index[df['id'] == track_id]) > 0
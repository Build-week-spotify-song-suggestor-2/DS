import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle

#for app 
# change '/content/' ====> './<name_of_folder_with__init__.py>/
filename = '/content/recommendation_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
songs_pkl = pd.read_pickle("/content/song_dataset.pkl")


def suggest_song_ids(track_id):
    # from track_id to audio_features
    song_index = songs_pkl.index[songs_pkl['id'] == track_id]
    audio_features = songs_pkl.iloc[song_index, 3:].to_numpy()
    # recommendation model
    distances, indices = loaded_model.kneighbors(audio_features)
    recommended_list = list(songs_pkl.loc[indices[0], 'id'])
  
    return recommended_list

list_o_ids = suggest_song_ids('2MuJbBWAVewREJmB8WdGJ3')
print(list_o_ids)
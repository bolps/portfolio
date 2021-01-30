import time
import argparse
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

parser = argparse.ArgumentParser(description='*** Spotify Feature Downloader ***')
parser.add_argument("--artist", required=True, type=str, help="")
args = parser.parse_args()

# Credenziali Spotify Developer
cid = 'f255839fe13348aab29eebc715b166b3'
secret = '4d4cfcf6b36f4ec0b3f1dddb89327257'
# Creo la sessione
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Creo una classe "song" per organizzare i dati scaricati dalle API
class song:
    def __init__(self, artist, name, uri, release_date, album, track_number, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence, popularity):
        self.artist = artist
        self.name = name
        self.uri = uri
        self.release_date = release_date 
        self.album = album
        self.track_number = track_number
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.tempo = tempo
        self.valence = valence
        self.popularity = popularity

    # Definisco un metodo per leggere i dati come dizionario
    def asDict(self):
        return {'artist': self.artist,
                'name': self.name, 
                'uri': self.uri, 
                'release_date': self.release_date,
                'album': self.album,
                'track_number': self.track_number,
                'acousticness': self.acousticness,
                'danceability': self.danceability,
                'energy': self.energy,
                'instrumentalness': self.instrumentalness,
                'liveness': self.liveness,
                'loudness': self.loudness,
                'speechiness': self.speechiness,
                'tempo': self.tempo,
                'valence': self.valence,
                'popularity': self.popularity}

# Cerco risultati per artista
name = args.artist
result = sp.search(name, type="artist") 

# Salvo URI e nome artista
artist_uri = result['artists']['items'][0]['uri']
artist_name = result['artists']['items'][0]['name']

# Attraverso l'URI dell'artista cerco gli album che ha pubblicato
artist_albums = sp.artist_albums(artist_uri, album_type='album')

# Salvo i nomi e l'URI di ogni singolo album dell'artista in liste separate
artist_album_names = []
artist_album_uris = []

for i in range(len(artist_albums['items'])):
    artist_album_names.append(artist_albums['items'][i]['name'])
    artist_album_uris.append(artist_albums['items'][i]['uri'])

# Creo un dizionario per corrispondenza album <-> uri album
album_dict = {artist_album_uris[i]: artist_album_names[i] for i in range(len(artist_album_uris))} 

# Creo una lista vuota in cui inserire le istanze "song"
songs = []

# Ottengo i dati attraverso le API
for album in artist_album_uris:
    tracks = sp.album_tracks(album)
    for track in tracks['items']:
        track_features = sp.audio_features(track['uri'])
        track_popularity = sp.track(track['uri'])
        songs.append(song(artist = artist_name, name = track['name'], uri = track['uri'], release_date = track_popularity['album']['release_date'], album = album_dict[album], track_number = track['track_number'], acousticness = track_features[0]['acousticness'], danceability = track_features[0]['danceability'], energy = track_features[0]["energy"], instrumentalness = track_features[0]['instrumentalness'], liveness = track_features[0]['liveness'], loudness = track_features[0]['loudness'], speechiness = track_features[0]['speechiness'], tempo = track_features[0]['tempo'], valence = track_features[0]['valence'], popularity = track_popularity['popularity']))
    # Inserisco un time.sleep per non superare il rate limit delle API
    time.sleep(3)

# Trasformo le istanze "song" in dizionari con il metodo asDict()
for i in range(len(songs)):
    songs[i] = songs[i].asDict()

# Creo il dataframe dalla lista di dizionari
df = pd.DataFrame(songs)

# Salvo il dataframe in un csv
df.to_csv("{}-SpotifyFeatures.csv".format(artist_name), index = False)

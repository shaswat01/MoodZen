from spotify_api import *

client_id = "718bb5e6caca403c942c2a292492ae64"
client_secret = "4980e48cec984e9aad21b60205c3f01b"

spotify = SpotifyAPI(client_id, client_secret)

def search_new_song(song_name, artist_name = '', DIR = 'src/data/'):

    search_result = spotify.base_search(song_name + ' ' + artist_name, search_type="track")
    
    if search_result['tracks']['total'] == 0:
        search_result = spotify.base_search(song_name, search_type="track")
        
    prev_url = search_result['tracks']['items'][0]['preview_url']
    
    if prev_url is None:
        return "Song Cannot Be Downloaded Using Spotify API"
    else:
        song_id = search_result['tracks']['items'][0]['id']
        track_name = search_result['tracks']['items'][0]['name']
        track_artist = search_result['tracks']['items'][0]['album']['artists'][0]['name']

        features = spotify.get_features(song_id)
        valence = features['valence']
        energy = features['energy']

        song_url = search_result['tracks']['items'][0]['external_urls']['spotify']

        wget.download(prev_url, DIR + song_id + '.wav')
        return song_id, track_name, track_artist, song_url, valence, energy
#!/usr/bin/python3
# Analyze the audio features of the tracks in a playlist

import spotipy
import json
import os
import time
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "user-library-read playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def get_playlist_id(playlist_name):
    current_user_id = sp.current_user()["id"]
    #print("Current user ID: ", current_user_id) # debug

    playlists = sp.user_playlists(user=current_user_id)
    if playlists["items"]:
        for playlist in playlists["items"]:
            if playlist["name"] == playlist_name:
                print("Playlist name: ",playlist["name"],"\nPlaylist ID: ", playlist["id"]) # debug
                return playlist["id"]

def get_playlist_tracks(playlist_id):
    # Get all tracks from the source playlist using pagination
    tracks = []
    offset = 0
    limit = 50  

    while True:
        results = sp.playlist_tracks(playlist_id=playlist_id, limit=limit, offset=offset)
        tracks.extend(results["items"])
        if len(results["items"]) < limit:
            #print("\nAll tracks fetched") #debug
            break
        offset += limit
        time.sleep(1) 
    
    track_dict = {}
    for index, track_info in enumerate(tracks):
        track_name = track_info["track"]["name"]
        #print(index, track_name) # debug
        track_uri = track_info["track"]["uri"]
        track_dict[index] = {"name": track_name, "uri": track_uri}

    return track_dict


def get_audio_features(track_dict):
    track_uris = [track["uri"] for track in track_dict.values()]
    audio_features = []

    batch_size = 50

    for i in range(0, len(track_uris), batch_size):
        batch_track_uris = track_uris[i:i + batch_size]
        batch_audio_features = sp.audio_features(batch_track_uris)

        for j, track_info in enumerate(batch_audio_features):
            track_name = track_dict[i + j]["name"]
            track_info["name"] = track_name

        audio_features.extend(batch_audio_features)

    return audio_features

def rank_tracks(audio_features, feature=input("Enter a feature to rank by: ")):
    ranked_tracks = sorted(audio_features, key=lambda x: x[feature], reverse=True)
    for index, track in enumerate(ranked_tracks):
        print((index+1 ), track["name"], track[feature])
    return ranked_tracks

if __name__ == "__main__":
    playlist_id = get_playlist_id("Liked Songs by kiwi")
    tracks = get_playlist_tracks(playlist_id)
    audio_features = get_audio_features(tracks)
    ranked_tracks = rank_tracks(audio_features)

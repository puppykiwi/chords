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
            print("\nAll tracks fetched")
            break
        offset += limit
        time.sleep(1) 
    
    track_dict = {}
    for index, track_info in enumerate(tracks):
        track_name = track_info["track"]["name"]
        track_uri = track_info["track"]["uri"]
        track_dict[index] = {"name": track_name, "uri": track_uri}

    return track_dict

def get_audio_features(track_dict):
    track_uris = [track["uri"] for track in track_dict.values()]
    audio_features = sp.audio_features(track_uris)
    print(audio_features) # debug
    return audio_features


if __name__ == "__main__":
    playlist_id = get_playlist_id("Indie Sounds")
    tracks = get_playlist_tracks(playlist_id)
    audio_features = get_audio_features(tracks)
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

def get_playlist_id(playlist_name):
    scope = "user-library-read playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


    current_user_id = sp.current_user()["id"]
    print("Current user ID: ", current_user_id) # debug

    playlists = sp.user_playlists(user=current_user_id)
    if playlists["items"]:
        for playlist in playlists["items"]:
            if playlist["name"] == playlist_name:
                print("Playlist name: ",playlist["name"],"\nPlaylist ID: ", playlist["id"]) # debug
                return playlist["id"]

get_playlist_id("Indie Sounds")
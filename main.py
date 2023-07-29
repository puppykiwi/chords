#!/usr/bin/python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "user-library-read playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))



def save_shortest_tracks_to_playlist(ource_playlist_name, new_playlist_name):
    # Initialize Spotipy client with OAuth2 authentication
    scope = "user-library-read playlist-modify-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Get the current user's ID
    current_user_id = sp.current_user()["id"]

    # Get the source playlist ID by searching for the playlist name
    source_playlist = None
    playlists = sp.current_user_playlists()
    for playlist in playlists["items"]:
        if playlist["name"] == source_playlist_name:
            source_playlist = playlist
            break

    if not source_playlist:
        print(f"Playlist '{source_playlist_name}' not found.")
        return

    # Create a new private playlist with the provided name
    new_playlist = sp.user_playlist_create(user=current_user_id, name=new_playlist_name, public=False)

    sp.playlist_add_items(playlist_id=new_playlist["id"], items=shortest_track_uris)

    print(f"The 20 shortest tracks from '{source_playlist_name}' have been added to the playlist '{new_playlist_name}'.")

# Example usage
if __name__ == "__main__":
    source_playlist_name = "My Shazam Tracks"
    new_playlist_name = "test1"


    save_shortest_tracks_to_playlist(source_playlist_name, new_playlist_name)

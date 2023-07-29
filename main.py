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
new_playlist_name = "Liked Songs by kiwi"

scope = "user-library-read playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


current_user_id = sp.current_user()["id"]
# Create a new private playlist with the provided name
new_playlist = sp.user_playlist_create(user=current_user_id, name=new_playlist_name, public=False)
# Get the user's saved tracks
saved_tracks = []
offset = 0
limit = 50  # Maximum number of tracks per API request
while True:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    saved_tracks.extend(results["items"])
    if len(results["items"]) < limit:
        # All saved tracks fetched
        break
    offset += limit
# Extract track URIs from the saved tracks
track_uris = [track["track"]["uri"] for track in saved_tracks]

for i in range(0, len(track_uris), 50):
        batch = track_uris[i:i + 50]
        sp.playlist_add_items(playlist_id=new_playlist["id"], items=batch)
        if i + 50 < len(track_uris):
            # Introduce a delay between consecutive calls to avoid rate limit
            time.sleep(1)
        

print(f"All saved tracks have been added to the playlist '{new_playlist_name}'.")
# Example usage

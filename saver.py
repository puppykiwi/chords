#/usr/bin/python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os

client_id="e86f9d7d6d0f4f429edd04bcca2fa5a1"
client_secret="c1a360cf401547058847e0c1a52955b3"
redirect_uri="http://localhost:3000"
new_playlist_name = "Liked Songs by kiwi"

# Initialize Spotipy client with OAuth2 authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="user-library-read playlist-modify-private"))
# Get the current user's ID
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
# Add the saved tracks to the new playlist
sp.playlist_add_items(playlist_id=new_playlist["id"], items=track_uris)
print(f"All saved tracks have been added to the playlist '{new_playlist_name}'.")
# Example usage

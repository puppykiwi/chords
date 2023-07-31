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

def get_playlist_id(playlist_name):
    scope = "user-library-read playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


    current_user_id = sp.current_user()["id"]

    playlists = sp.user_playlists(user=current_user_id)
    if playlists["items"]:
        for playlist in playlists["items"]:
            print(playlist["name"]) # debug
            if playlist["name"] == playlist_name:
                print("Playlist ID: ", playlist["id"]) # debug
                return playlist["id"]

def add_shortest_songs_to_existing_playlist(source_playlist_id, destination_playlist_id):
    # Initialize Spotipy client with OAuth2 authentication
    scope = "user-library-read playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    # Get all tracks from the source playlist using pagination
    tracks = []
    offset = 0
    limit = 100  # Maximum number of tracks per API request

    while True:
        results = sp.playlist_tracks(playlist_id=source_playlist_id, limit=limit, offset=offset)
        tracks.extend(results["items"])
        if len(results["items"]) < limit:
            # All tracks fetched
            break
        offset += limit
        time.sleep(1)  # Add a 1-second delay between requests to stay within the rate limit

    # Sort tracks by duration (length)
    sorted_tracks = sorted(tracks, key=lambda x: x["track"]["duration_ms"])

    # Extract track URIs for the 20 shortest songs
    shortest_tracks = sorted_tracks[:5]
    track_uris = [track["track"]["uri"] for track in shortest_tracks]

    # Add the 20 shortest songs to the existing destination playlist
    total_tracks = len(track_uris)
    batch_size = 100  # Maximum number of tracks per API request to add to the playlist

    for i in range(0, total_tracks, batch_size):
        sp.playlist_add_items(playlist_id=destination_playlist_id, items=track_uris[i:i+batch_size])
        time.sleep(1)  # Add a 1-second delay between batch requests to stay within the rate limit

    print(f"The 20 shortest songs have been added to the playlist with ID '{destination_playlist_id}'.")

# Example usage
if __name__ == "__main__":
    
    source_playlist_id = "7eG04lBozqMlzgmpM1omp3"
    destination_playlist_id = "7jdMbtN1NnbULSStIOZG8n"

    add_shortest_songs_to_existing_playlist(source_playlist_id, destination_playlist_id)
import os
import keyboard
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load Spotify API credentials from .env file
from dotenv import load_dotenv
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_CLIENT_REDIRECT_URI = os.getenv('SPOTIPY_CLIENT_REDIRECT_URI')

# Check if credentials are available
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise ValueError("Please provide Spotify API credentials in the .env file.")

# Set up Spotify authentication using Authorization Code Flow
# SpotifyOAuth is used as Spotify credentials don't provide specific authentication for premium status
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='user-modify-playback-state, user-read-currently-playing, user-read-playback-state'
                                               ))

# Initial volume value
curr_volume_value = 30  # Set to starting volume, keep low to avoid blowing out ears
curr_playback_status = True

def update_volume():
    """Update the Spotify playback volume."""
    sp.volume(volume_percent=curr_volume_value)

def open_spotify_web_page():
    """Open the Spotify web page in the default web browser."""
    webbrowser.open('https://open.spotify.com/', new=2)
    print('Opening Spotify web app')

def print_controls():
    """Print the available controls."""
    print("Controls:")
    print("Num 8: Increase volume")
    print("Num 5: Decrease volume")
    print("Num 6: Next track")
    print("Num 4: Previous track")
    print("Num 9: Play/Pause")
    print("Num Enter: Open Spotify web page")
    print("F10: Exit")

def print_track():
    track_info = sp.current_playback()
    if track_info and 'item' in track_info:
        current_track = track_info['item']
        return f"Current Track: {current_track['name']} (ID: {current_track['id']})"
    else:
        return "No track is currently playing."


def on_key_event(e):
    """Handle keyboard events."""
    global curr_volume_value, curr_playback_status

    if e.event_type == keyboard.KEY_DOWN:
        if e.scan_code == 72:  # Num 8
            curr_volume_value = min(100, curr_volume_value + 10)
            update_volume()
            print('Volume increased to', curr_volume_value)
        elif e.scan_code == 76:  # Num 5
            curr_volume_value = max(0, curr_volume_value - 10)
            update_volume()
            print('Volume decreased to', curr_volume_value)
        elif e.scan_code == 77:  # Num 6
            sp.next_track()
            curr_track = print_track()
            print(curr_track)
        elif e.scan_code == 75:  # Num 4
            sp.previous_track()
            curr_track = print_track()
            print(curr_track)
        elif e.scan_code == 82:  # Num 0
            if curr_playback_status:
                sp.pause_playback()
                curr_playback_status = False
                print('Playback paused, press Num 0 to resume')
            else:
                sp.start_playback()
                curr_playback_status = True
                print('Playback unpaused, press Num 0 to pause')
        elif e.scan_code == 156:  # Num Enter
            open_spotify_web_page()

# Print controls upon opening
print_controls()

# Set initial volume
update_volume()
sp.start_playback()
# Set up keyboard hook
keyboard.hook(on_key_event)

# Wait for user to press 'F10' to exit
keyboard.wait('f10')
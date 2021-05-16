import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from PIL import Image
from pathlib import Path
from io import BytesIO
import requests
import palettes
import json


spotify_path = Path("Spotify Images/")

with open("test_data_1.json", "r") as fp:
    song_dict = json.load(fp)

# For each song retrieve the cover image from the URL
# Format song name -> valid file name and save image
# Add filename to the song in song dictionary
for song in song_dict:
    name = song_dict[song]['name']
    filename = "".join( x for x in name if (x.isalnum() or x in "_- "))
    url = (song_dict[song]['url'])

    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(str(spotify_path / (filename + ".png")))

    song_dict[song]['filename'] = filename + ".png"

# Version is the pre-fix used on saved images
version = "V1"

songs = palettes.Songs(song_dict, version)

# Generate thumbnail images (100px, 100px) for each song
songs.generateThumbnailImages()

# Calculate the colour palette of each song's cover image
songs.generatePalettes()

# Create image of sorted colours arranged in a grid
songs.createGridImage()

# Create a GIF displaying palette + each song cover
songs.generateAnimation()

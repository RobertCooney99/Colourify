# Colourify

<img src="https://raw.githubusercontent.com/RobertCooney99/Colourify/main/Images/Logo-V3-LARGE.png" width="100" height="100">

**Colourify** is a Python program that analyses the colour schemes of the album covers taken from a users Spotify listening history. Each song produces an 8 colour palette containing the most
dominant colours within the image. In **Version 1** the program creates a list of all the colours from the calculated palettes and categorises the colours into 8 sets based on
the Hue value of the colour. Each individual Hue category is then sorted based on the luminosity value.

## Future Versions

In the next version of **Colourify** the program will be converted into a web application in which user's can connect their Spotify accounts and receive a number of graphs and
different formats of data representations displaying their listening history colour palette.

Following this, content sharing features will be added to aid the user in uploading their results to social media. Once this has been added the application will be expanded to
allow the user to choose one of their created playlists to colour analyse.

In the future the application will also track the Top 50 charts of different nations around the world to produce an animation that shows the evolution of album cover art colour
palettes over time.

## Using Colourify

Colourify uses a number of Python packages;
- spotipy
- cred
- PIL (Python Imaging Library)
- pathlib
- io
- requests
- json
- numpy
- math
- colorsys

The code uploaded to GitHub makes use of the test-data provided in the **.json** file.

## Example Song Palettes

| **Shoot You Down - The Stone Roses** | **Sola Es Mejor - Karol G** | **Flying On The Ground - Noel Gallagher** |
| :----------------------------------: | :-------------------------: | :---------------------------------------: |
| ![Cover Palette](https://raw.githubusercontent.com/RobertCooney99/Colourify/main/Images/Palette%20-%20Shoot%20You%20Down%20-%20Remastered.png) | ![Cover Palette](https://raw.githubusercontent.com/RobertCooney99/Colourify/main/Images/Palette%20-%20SOLA%20ES%20MEJOR.png) | ![Cover Palette](https://raw.githubusercontent.com/RobertCooney99/Colourify/main/Images/Palette%20-%20Flying%20On%20The%20Ground.png) |

## Example Listening History Palette

![Example palette](https://raw.githubusercontent.com/RobertCooney99/Colourify/main/Images/V2%20-%20Palette.png)

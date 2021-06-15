from PIL import Image
from pathlib import Path
import numpy
import math
import colorsys

# Set file paths
image_path = Path("Spotify Images/")
thumbnail_path = Path("Spotify Thumbnails/")
palette_path = Path("Spotify Palettes/")
animation_path = Path("Animation Images/")

thumnbail_size = 100, 100

bands_str_to_int = {"RED": 0, "GREEN": 1, "BLUE": 2}
bands_int_to_str = {0: "RED", 1: "GREEN", 2: "BLUE"}

# Size (#. of colours) of palette for each cover image
depth = 8


class Songs():

    def __init__(self, song_dict, version):
        self.version = version
        self.song_dict = song_dict
        self.num_of_songs = len(self.song_dict)
        self.palette_manager = Palette(version)
        self.colour_id = 0

    def getNewColourID(self):
        self.colour_id += 1
        return self.colour_id

    def printSongs(self):
        # Print song dictionary
        for song in self.song_dict:
            print(self.song_dict[song])

    def generateThumbnailImages(self):
        for song in self.song_dict:
            generateThumbnailImage(self.song_dict[song])

    def generatePalettes(self):
        for song in self.song_dict:
            # Calculate the song's cover image colour palette
            calculatePalette(self.song_dict[song])
            # Create and save an image displaying cover image + palette
            generatePaletteImage(self.song_dict[song])

            # Create a dictionary of colours for this song
            colour_dict = {}
            for colour in self.song_dict[song]['palette']:
                # Add Unique Colour ID : colour to dictionary
                colour_dict[self.getNewColourID()] = colour
            
            self.song_dict[song]['colours'] = colour_dict

        self.populatePalette()
        self.sortPalette()

    def populatePalette(self):
        for song in self.song_dict:
            for colour in self.song_dict[song]['colours']:
                rgb_colour = self.song_dict[song]['colours'][colour]
                self.palette_manager.addColour(rgb_colour, song, colour)

    def sortPalette(self):
        self.palette_manager.sortColours()

    def printPalette(self):
        self.palette_manager.printPalette()

    def createGridImage(self, dimension=25, columns=16):
        self.palette_image = self.palette_manager.visualisePaletteGrid(dimension, columns)

    def printSongColourPositions(self):
        # Output the details of each song
        # For each song output each colour and the colour's index in the sorted list
        for song in self.song_dict:
            song_name = self.song_dict[song]['name']
            artist_name = self.song_dict[song]['artist']
            song_id = song
            print("--------------")
            print("{}. {} - {}".format(song_id, artist_name, song_name))
            for colour_id in self.song_dict[song]['colours']:
                colour_value = self.song_dict[song]['colours'][colour_id]
                colour_sorted_index = self.palette_manager.getColourPositionByID(colour_id)
                print("COL #{}: {} - Position: {}".format(colour_id, colour_value, colour_sorted_index))
            print("--------------")

    def generateAnimation(self):
        image_frames = []

        frame_width = self.palette_image.size[0] + 300
        frame_height = max(self.palette_image.size[1], 275)

        first_frame = self.generateFirstAnimationFrame(frame_width, frame_height)
        # Add more of the first frame to extend duration in .gif
        for i in range(0, 3):
            image_frames.append(first_frame)

        # Calculate position in image to place palette image
        # palette image is the song cover image & palette
        palette_image_x_position = int(self.palette_image.size[0] + ((300-200)/2))
        palette_image_y_position = int((frame_height/2) - (225/2))
        palette_image_pos = (palette_image_x_position, palette_image_y_position)
        for song in self.song_dict:
            image_frames.append(self.generateAnimationFrame(song, frame_width, frame_height, palette_image_pos))

        # Save all frames in a .gif
        start_frame = image_frames[0].copy()
        start_frame.save(str(animation_path / (self.version + " - Palette Animation.gif")), save_all=True, append_images=image_frames[1:], duration=300, loop=0)

    def generateFirstAnimationFrame(self, frame_width, frame_height):
        # Start frame is all the song's palettes on a blank background
        start_frame = Image.new("RGBA", (frame_width, frame_height), (255,255,255,255))

        start_frame.paste(self.palette_image, (0, 0))

        return start_frame

    def generateAnimationFrame(self, song, frame_width, frame_height, palette_image_pos):
        # Add the song cover image and song's palette to image
        frame = Image.new("RGBA", (frame_width, frame_height), (255,255,255,255))

        song_filename = self.song_dict[song]['filename']
        song_palette_image = Image.open(str(palette_path / ("Palette - " + song_filename)))

        frame.paste(self.palette_image, (0, 0))
        frame.paste(song_palette_image, palette_image_pos)

        return frame        


class Palette():

    def __init__(self, version):
        self.version = version
        self.colours = []
        self.sorted_colours = []
        self.palette_image_name = self.version + " - Palette.png"

    def setPaletteImageName(self, name):
        self.palette_image_name = self.version + " - " + name

    def addColour(self, colour, song_id, colour_id):
        self.colours.append([colour, colour_id, song_id])

    def printPalette(self):
        for colour in self.colours:
            print("{}: CID #{} - SID #{}".format(colour[0], colour[1], colour[2]))

    def sortColours(self):
        # Sort list of colours
        # Sorts colours into 8 categories of "hue"
        # Sorts each category of hue based on colour luminosity value
        # Every second category is flipped to provide smooth transition between categories
        self.colours = sorted(self.colours, key=lambda colour: groupHSVDenoise(colour[0], 8))

    def getColourPositionByID(self, colour_id):
        # Return the index of a specific colour ID in the sorted colour list
        index_counter = 0
        for colour in self.colours:
            if (colour[1] == colour_id):
                return index_counter
            index_counter += 1

    def visualisePaletteGrid(self, dimension, columns):
        # Generate the image of all the colours in a grid
        square_dim = dimension
        colours_per_row = columns

        # Calculate required width & height to display image
        image_height = int(square_dim * math.ceil((len(self.colours) / colours_per_row)))
        image_width = int(colours_per_row * square_dim)

        palette_image = Image.new("RGB", (image_width, image_height), (0,0,0))

        counter = 0
        for colour in self.colours:
            # Add a square of each colour to the image
            rgb_colour = colour[0]
            colour_image = Image.new("RGB", (square_dim, square_dim), rgb_colour)
            column = counter % colours_per_row
            row = math.floor(counter/colours_per_row)
            if ((row % 2) == 1):
                column = colours_per_row - 1 - column
            palette_image.paste(colour_image, (column * square_dim, row * square_dim))
            counter += 1

        palette_image.save(str(palette_path / (self.palette_image_name)))
        return palette_image


def groupHSVDenoise(rgb, repetitions=1):
    # Convert RGB to HSV
    r, g, b = rgb
    l = lum(r, g, b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Change HSV values from float(0-1) to int(0-(depth-1))
    h2 = int(h * repetitions)
    l2 = int(l * repetitions)
    v2 = int(v * repetitions)

    if h2 % 2 == 1:
        v2 = repetitions - v2
        l = repetitions - l

    return (h2, l, v2)


def lum(r, g, b):
    # Calculate luminosity of RGB value
    return math.sqrt(.241 * r + .691 * g + .068 * b)


def getWidestBand(list_of_pixels):
    # Return widest range (R, G or B) from a list of RGB values
    red = list_of_pixels[:, 0]
    green = list_of_pixels[:, 1]
    blue = list_of_pixels[:, 2]

    ranges = [getBandRange(red), getBandRange(green), getBandRange(blue)]

    max_range = max(ranges)

    return ranges.index(max_range)


def getBandRange(band):
    # Calculate range of a colour band (R/G/B)
    return max(band) - min(band)


def splitList(pixel_list):
    half = len(pixel_list)//2
    return pixel_list[:half], pixel_list[half:]


def averageList(pixel_list):
    # Average a list of RGB values
    red_total = 0
    green_total = 0
    blue_total = 0
    num_of_pixels = len(pixel_list)

    for pixel in pixel_list:
        red_total += pixel[0]
        green_total += pixel[1]
        blue_total += pixel[2]

    red_avg = red_total / num_of_pixels
    green_avg = green_total / num_of_pixels
    blue_avg = blue_total / num_of_pixels

    rgb_colour = (int(red_avg), int(green_avg), int(blue_avg))
    return rgb_colour


def getBuckets(image_pixels):
    # Find band with largest range (R/G/B) in the bucket
    max_range_band = getWidestBand(image_pixels)
    # Sort the bucket by the band with largest range
    sorted_pixels = sorted(image_pixels, key= lambda x: x[max_range_band])
    # Split bucket into two
    list_1, list_2 = splitList(sorted_pixels)

    return numpy.asarray(list_1), numpy.asarray(list_2)


def calculatePalette(song):
    image_name = song['filename']
    image = Image.open(str(thumbnail_path / ("Thumbnail - " + image_name)))
    image = image.convert("RGB")

    # Put all image pixels into a bucket
    image_pixels = numpy.asarray(image.getdata())
    buckets = [image_pixels]
    palette = []

    # Split bucket of pixels until number of buckets = depth
    while len(buckets) != depth:
        new_buckets = []
        for bucket in buckets:
            list_1, list_2 = getBuckets(bucket)
            new_buckets.append(list_1)
            new_buckets.append(list_2)
        buckets = new_buckets

    # Get the average colour of each bucket and add average colour to palette
    for bucket in buckets:
        palette.append(averageList(bucket))

    # Set the song's colour palette
    song['palette'] = palette


def generatePaletteImage(song):
    image_width = len(song['palette']) * 25
    image_height = 225
    image_name = song['filename']
    palette_image = Image.new("RGB", (image_width, image_height), (0,0,0))

    counter = 0
    for rgb_colour in song['palette']:
        colour_image = Image.new("RGB", (25, 25), rgb_colour)
        palette_image.paste(colour_image, ((counter*25),0))
        counter += 1

    song_image = Image.open(str(thumbnail_path / ("Thumbnail - " + image_name)))
    palette_image.paste(song_image, (50,75))

    palette_image.save(str(palette_path / ("Palette - " + image_name)))
    song['palette_image'] = True


def generateThumbnailImage(song):
    image_name = song['filename']
    image = Image.open(str(image_path / image_name))

    image.thumbnail(thumnbail_size)
    image = image.convert("RGB")
    image.save(str(thumbnail_path / ("Thumbnail - " + image_name)))
    song['thumbnail'] = True

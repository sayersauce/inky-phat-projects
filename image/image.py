# Max Sayer
# https://max.lat
import time
import os
import random
from inky import InkyPHAT
from PIL import Image

display = InkyPHAT("red")
path = os.path.dirname(__file__) + "images/"
dirs = os.listdir(path)

def display_image():
    image = Image.open(path + dirs[random.randrange(len(dirs))])
    image = image.resize((display.WIDTH, display.HEIGHT), 0)
    image = image.convert("1")
    display.set_image(image.rotate(180))
    display.show()

while True:
    display_image()
    time.sleep(5)
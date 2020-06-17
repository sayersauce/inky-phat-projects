# Max Sayer
# https://max.lat
import time
import os
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime


display = InkyPHAT("red")
path = os.path.dirname(__file__)
large = ImageFont.truetype(path + "/WindyCity.ttf", 18)
normal = ImageFont.truetype(path + "/WindyCity.ttf", 12)
display.set_border(display.WHITE)


# Draws text to the display 
def draw_text(draw, text, x, y, font, col = display.BLACK):
    draw.text((x, y), text, col, font)


# Sends the image to the display
def update_display(image):
    display.set_image(image.rotate(180))
    display.show()


# Display start-up text
def startup_text():
    image = Image.new("P", (display.WIDTH, display.HEIGHT))
    draw = ImageDraw.Draw(image)

    w, h = large.getsize("Hello")
    draw_text(draw, "Hello", (display.WIDTH / 2) - (w / 2), (display.HEIGHT / 2) - (h / 2) - 10, large)

    datetext = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw_text(draw, datetext, (display.WIDTH / 2) - (normal.getsize(datetext)[0] / 2), (display.HEIGHT / 2) - (h / 2) + 10, normal)

    update_display(image)
    

# Display raspberrypi information
def information_text():
    image = Image.new("P", (display.WIDTH, display.HEIGHT))
    draw = ImageDraw.Draw(image)

    # Date and Time
    datetext = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw_text(draw, datetext, 5, 5, normal, display.RED)

    # CPU
    temperature = "CPU " + cpu_usage() + "% " + cpu_temp() + "C"
    draw_text(draw, temperature, 5, 25, large)

    # RAM
    ramarr = ram()
    ramtext = "RAM " + ramarr[1] + " / " + ramarr[0]
    draw_text(draw, ramtext, 5, 50, large)

    # DISK
    diskarr = disk()
    disktext = "DISK " + diskarr[1] + "B / " + diskarr[0] + "B"
    draw_text(draw, disktext, 5, 75, large)

    update_display(image)


# https://gist.github.com/funvill/5252169#file-gistfile1-py


def cpu_usage():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))


def cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    return(res.replace("temp=","").replace("'C\n",""))


def format_ram(r):
    # Assumes RAM is 3 digits or below, made for Pi Zero W
    r = str(int(r)/1000)
    if r[2] == ".": return r[0:2] + "MB"
    return r[0:3] + "MB"


def ram():
    p = os.popen("free")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return [format_ram(i) for i in line.split()[1:4]]


def disk():
    p = os.popen("df -h /")
    i = 0
    while True:
        i = i + 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:4])


if __name__ == "__main__":
    startup_text()
    time.sleep(20)
    while True:
        information_text()
        time.sleep(30)

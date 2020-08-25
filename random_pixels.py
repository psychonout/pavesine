"""
    This is a Python3 code that does the lightshow for a led strip
"""
import time
import board
import neopixel
import json
import os
#from bulb import set_color as set_bulb_color
from random import randint, choice
from pprint import pprint

try:
    pixels = 900
    blank = [0, 0, 0]
    strip = neopixel.NeoPixel(board.D18,
    			   pixels,
    			   auto_write=False,
    			   pixel_order=neopixel.RGB)
    print("Strip initialized!")
except Exception as e:
    print(e)


def generator(size, direction="fwd"):
    if direction == "fwd":
        return (
            number
            for number in range(size)
        )
    elif direction == "bck":
        return (
            number
            for number in reversed(range(size))
        )

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return [pos * 3, 255 - pos * 3, 0]
    elif pos < 170:
        pos -= 85
        return [255 - pos * 3, 0, pos * 3]
    else:
        pos -= 170
        return [0, pos * 3, 255 - pos * 3]


def clear_strip():
    for i in generator(pixels):
        strip[i] = blank
    strip.show()


def color_wipe(color=blank, delay=0, direction="fwd"):
    for i in generator(pixels, direction):
        strip[i] = color
        strip.show()
       #  time.sleep(delay)


def color_both_sides(color=blank, delay=0, direction="fwd"):
    for i in generator(int(pixels/2), direction):
        strip[i] = color
        strip[pixels-i-1] = color
        strip.show()
        # time.sleep(delay)


def both_sides_two_colors(color1=blank, color2=blank, direction="fwd"):
    for i in generator(int(pixels/2), direction):
        strip[i] = color1
        strip[pixels-i-1] = color2
        strip.show()


def theater_chase(color=blank, delay=0, iterations=10, direction="fwd"):
    """Movie theater light style chaser animation."""
    for j in generator(iterations):
        for q in generator(3):
            for i in range(0, pixels, 3):
                strip[i+q] = color
            strip.show()
            time.sleep(delay/10)
            for i in range(0, pixels, 3):
                strip[i+q] = blank


def rainbow(delay=0, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in generator(256*iterations):
        for i in generator(pixels):
            color = wheel((i+j) & 255)
            strip[i] = color
        strip.show()
        time.sleep(delay)


def rainbow_cycle(delay=0, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in generator(256*iterations):
        for i in generator(pixels):
            color = wheel((int(i * 256 / pixels + j) & 255))
            strip[i] = color
        strip.show()
        time.sleep(delay)


def theater_chase_rainbow(delay=0, iterations=10):
    """Rainbow movie theater light style chaser animation."""
    for j in generator(iterations):
        for q in generator(3):
            for i in range(0, pixels, 3):
                color = wheel((i+j) % 255)
                strip[i+q] = color
            strip.show()
            time.sleep(delay*100)
            for i in range(0, pixels, 3):
                strip[i+q] = blank


def pulse(color, delay=0, iterations=3):
    # rgb - find lowest value
    # find multipliers for all other values
    # iterate all accordingly
    # could also try using w
    for iteration in range(iterations):
        pass


def bulb_flow():
    # adding this to separate process, but could probably do async
    try:
        py3 = "/usr/bin/python3"
        script = os.path.join(os.getcwd(), "set_flow.py")
        os.system(f"{py3} {script}")
    except Exception:
        pass


def run_pixels(shade=None):
    with open("colors.json", "r") as f:
        colors = json.load(f)
    while True:
        # how many times functions repeat in different settings
        times = 2
        funk = [color_wipe] * times
        funk.extend([color_both_sides] * times)
        funk.extend([theater_chase] * times * times)
        for i, fn in enumerate(funk):
            color = choice(colors)
            print(color["name"])
            if shade:
                while shade not in color["name"].lower():
                    color = choice(colors)
            color = color["rgb"]
            try:
                set_bulb_color(color)
            except Exception:
                pass
            # strip interprets colors differently, r and g switched
            color = [color[1], color[0], color[2]]
            if i >= times * 2:
                fn(color, delay=randint(1, 5))
            elif i % times == 0:
                fn(color)
                fn()
            elif i+1 % times == 0:
                fn(color, direction="bck")
                fn(direction="bck")
            # these two below dont work correctly
            elif i+2 % times == 0:
                fn(color)
                fn(direction="bck")
            else:
                fn(color, direction="bck")
                fn()
        if not shade:
            # process = bulb_flow()
            for fn in [rainbow, rainbow_cycle, theater_chase_rainbow]:
                fn()
            color1 = choice(colors)["rgb"]
            color2 = choice(colors)["rgb"]
            both_sides_two_colors(color1, color2, "fwd")
            both_sides_two_colors([0, 0, 255], [0, 255, 0], "bck")

if __name__ == "__main__":
    while True:
        both_sides_two_colors([0, 255, 0], [0, 0, 255], "fwd")
        both_sides_two_colors([0, 0, 255], [0, 255, 0], "bck")
        both_sides_two_colors()
        run_pixels()

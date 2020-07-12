"""
    This is a Python3 code that does the lightshow for a led strip
"""
import time
import board
import neopixel
import json
import os
from bulb import set_color as set_bulb_color
from random import randint, choice
from pprint import pprint

pixels = 300
blank = [0, 0, 0]
strip = neopixel.NeoPixel(board.D18,
			   pixels,
			   auto_write=False,
			   pixel_order=neopixel.RGB)


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


def run_pixels():
    with open("colors.json", "r") as f:
        colors = json.load(f)
    while True:
        for i, fn in enumerate([color_wipe, color_wipe, color_both_sides,
                                color_both_sides, theater_chase]):
            color = choice(colors)
            try:
                set_bulb_color(color["rgb"])
                print(color["name"])
            except Exception:
                pass
            # strip interprets colors differently
            color["rgb"] = [color["rgb"][1], color["rgb"][0], color["rgb"][2]]
            if i % 2 == 0:
                if i == 4:
                    fn(color["rgb"], delay=1)
                else:
                    fn(color["rgb"])
                    fn()
            else:
                fn(color["rgb"], direction="bck")
                fn(direction="bck")
        color_both_sides(color["rgb"])
        color_both_sides(direction="bck")        
        # process = bulb_flow()
        for fn in [rainbow, rainbow_cycle, theater_chase_rainbow]:
            fn()
        # process.terminate()


if __name__ == "__main__":
    run_pixels()

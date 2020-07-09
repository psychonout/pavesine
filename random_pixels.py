"""
    This is a Python3 code
"""
import time
import board
import neopixel
import json
from random import randint, choice
from pprint import pprint

pixels = 300
blank = [0, 0, 0, 0]
strip = neopixel.NeoPixel(board.D18,
			   pixels,
			   auto_write=False,
			   pixel_order=neopixel.RGBW)


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
        time.sleep(delay)


def color_both_sides(color=blank, delay=0, direction="fwd"):
    for i in generator(int(pixels/2), direction):
        strip[i] = color
        strip[pixels-i-1] = color
        strip.show()
        time.sleep(delay)


def theater_chase(color=blank, delay=0, iterations=10, direction="fwd"):
    """Movie theater light style chaser animation."""
    for j in generator(iterations):
        for q in generator(3):
            for i in range(0, pixels, 3):
                strip[i+q] = color
            strip.show()
            time.sleep(delay*100)
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
                strip[i+q] = _color
            strip.show()
            time.sleep(delay*100)
            for i in range(0, pixels(), 3):
                strip[i+q] = blank


def pulse(color, delay=0, iterations=3):
    # rgb - find lowest value
    # find multipliers for all other values
    # iterate all accordingly
    # could also try using w
    for iteration in range(iterations):
        pass



if __name__ == "__main__":
    with open("colors.json", "r") as f:
        colors = json.load(f)
    while True:
        for i, fn in enumerate([color_wipe, color_wipe, color_both_sides,
                                color_both_sides, theater_chase]):
            rand_color = choice(colors)
            print(rand_color["name"])
            if i % 2 == 0:
                fn(rand_color["rgb"])
                fn()
            else:
                fn(rand_color["rgb"], direction="bck")
                fn(direction="bck")
        for fn in [rainbow, rainbow_cycle, theater_chase_rainbow]:
            fn()
            clear_strip()

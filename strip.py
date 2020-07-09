#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
from random import randint
import subprocess
from os import system

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
WAIT           = 10.0 / 10000.0


def make_color(color):
    # the colors are swapped, because the led strip is GRB
    return Color(color[1], color[0], color[2])


def pulse(strip, color, wait_ms=WAIT, iterations=3):
	for iter in range(iterations):
		temp = 0
		while temp != color[0]:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, make_color([temp, temp, temp]))
			strip.show()
			temp += 1
		temp = color[0]
		while temp != 0:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, make_color([temp, temp, temp]))
			strip.show()
			temp -= 1


def theaterChase(strip, color, wait_ms=WAIT, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, make_color(color))
            strip.show()
            time.sleep(wait_ms*100)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


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


def rainbow(strip, wait_ms=WAIT, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            color = wheel((i+j) & 255)
            strip.setPixelColor(i, make_color(color))
        strip.show()
        time.sleep(wait_ms)


def rainbowCycle(strip, wait_ms=WAIT, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            color = wheel((int(i * 256 / strip.numPixels()) + j) & 255)
            strip.setPixelColor(i, make_color(color))
        strip.show()
        time.sleep(wait_ms)


def theaterChaseRainbow(strip, wait_ms=WAIT):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                color = wheel((i+j) % 255)
                strip.setPixelColor(i+q, make_color(color))
            strip.show()
            time.sleep(wait_ms)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def bulb(color):
    try:
        py3 = '/usr/bin/python3'
        system('{} /home/pi/set_rgb.py {} {} {}'.format(py3, color[0],
                                                        color[1], color[2]))
    except Exception:
        pass


def flow():
    try:
        py3 = '/usr/bin/python3'
        return subprocess.Popen([py3, '/home/pi/set_flow.py'])
    except Exception:
        pass


def init_pixel():
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                              LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    return strip


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear',
                        action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    # Create NeoPixel object with appropriate configuration.
    strip = init_pixel()
    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print('Wait time ' + str(WAIT) + 'ms')
            colors = [[255, 0, 0], [255, 255, 0], [0, 255, 0],
		      [0, 255, 255], [0, 0, 255], [255, 0, 255], [255, 255, 255]] 
            for color in colors:
                bulb(color)
		pulse(strip, color, WAIT)
		colorWipe(strip, color, WAIT)  # Red wipe
		colorWipe(strip)
		color_wipe_reversed(strip, color, WAIT)
		color_wipe_reversed(strip)
		color_double(strip, color, WAIT)
		color_double(strip)
		theaterChase(strip, color)
            # process = flow()
            # print('Rainbow animations.')
            # rainbow(strip)
            # print('Rainbow cycle animations.')
            # rainbowCycle(strip)
            # print('Theater Chase Rainbow animations.')
            # theaterChaseRainbow(strip)
            # process.terminate()

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, [0, 0, 0], 10)
            bulb(color)

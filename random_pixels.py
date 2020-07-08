import time
import board
import neopixel
from random import randint

pixels = neopixel.NeoPixel(board.D18, 300, auto_write=False, pixel_order=neopixel.RGBW)
while True:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    w = randint(0, 255)
    for pixel in range(len(pixels)):
        # print(r, g, b, w)
        pixels[pixel] = (r, g, b, w)
    pixels.show()
    time.sleep(1)
    for pixel in range(len(pixels)):
        pixels[pixel] = (0, 0, 0, 0)
    pixels.show()

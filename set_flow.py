import time
from bulb import set_color
from random_pixel import wheel


if __name__ == "__main__":
    wait_ms = 50
    while True:
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256):
            i = 0
            color = wheel((i+j) & 255)
            bulb.set_rgb(color)
            time.sleep(wait_ms/1000.0)

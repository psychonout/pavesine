from strip import init_pixel, colorWipe


def clear_strip():
    strip = init_pixel()
    colorWipe(strip, [0, 0, 0], 10)


if __name__ == "__main__":
    clear_strip()

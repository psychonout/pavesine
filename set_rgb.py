import sys
from bulb import set_color


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Incorrect number of arguments")
        sys.exit()
    color = []
    for i in sys.argv[1:]:
        color.append(int(i))
    set_color(color)

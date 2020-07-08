from miio import Yeelight


def init():
    ip = '192.168.0.55'
    token = '036f6ef3fb6f08c8aace35ade458c05d'
    return Yeelight(ip, token)


def turn_on():
    bulb = init()
    bulb.on()


def turn_off():
    bulb = init()
    bulb.off()


def set_color(color):
    bulb = init()
    bulb.set_rgb(color)


def set_brightness(level, transition):
    bulb = init()
    bulb.set_brightness(level, transition)


def set_color_temp(temp):
    bulb = init()
    bulb.set_color_temp(temp)


if __name__ == "__main__":
    bulb = init()
    print(bulb.status())
    set_brightness(100, 3000)

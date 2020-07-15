from miio import Yeelight


ip = '192.168.0.55'
token = '036f6ef3fb6f08c8aace35ade458c05d'
itam = Yeelight(ip, token)


def turn_on():
    itam.on()


def turn_off():
    itam.off()


def set_color(color):
    itam.set_rgb(color)


def set_brightness(level, transition):
    itam.set_brightness(level, transition)


def set_color_temp(temp):
    itam.set_color_temp(temp)


if __name__ == "__main__":
    print(itam.status())
    itam.set_brightness(100, 3000)

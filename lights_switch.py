import sys
import subprocess
import bulb
from tasmota import query
from random_pixels import run_pixels, clear_strip


tasmota_led_strip = "http://192.168.0.166"
tasmota_power_source = "http://192.168.0.127"

def make_it(color):
    lights_out()
    try:
        bulb.turn_on()
    except Exception:
        pass
    query(tasmota_power_source, "power on")
    run_pixels(color)


def lights_in():
    lights_out()
    try:
        bulb.turn_on()
    except Exception:
        pass
    query(tasmota_led_strip, "power on")
    query(tasmota_power_source, "power on")    
    run_pixels()


def lights_out():
    try:
        bulb.turn_off()
    except Exception:
        pass
    clear_strip()
    query(tasmota_led_strip, "power off")
    query(tasmota_power_source, "power off")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "sunrise":
            lights_out()
        elif sys.argv[1] == "sunset":
            lights_in()
    else:
        sys.exit("""This program accepts 'sunrise', 'sunset' arguments.""")

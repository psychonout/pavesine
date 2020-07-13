import sys
import subprocess
from bulb import turn_on, turn_off
from tasmota import query
from random_pixels import run_pixels, clear_strip


tasmota_led_strip = "http://192.168.0.196"
tasmota_power_source = "http://192.168.0.23"


def lights_in():
    try:
        turn_on()
    except Exception:
        pass
    query(tasmota_led_strip, "power on")
    query(tasmota_power_source, "power on")    
    run_pixels()


def lights_out():
    try:
        turn_off()
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

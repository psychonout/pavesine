from bulb import turn_on
from tasmota import query
import subprocess


if __name__ == '__main__':
    turn_on()
    query("http://192.168.0.196", "power on")
    # subprocess.Popen(["pkill", 'python'])
    subprocess.Popen(['/usr/bin/python',
                      '/home/pi/strip.py'])
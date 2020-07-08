from bulb import turn_off
from tasmota import query
import subprocess


if __name__ == '__main__':
    turn_off()
    query("http://192.168.0.196", "power off")
    subprocess.Popen(['/usr/bin/python',
                      '/home/pi/strip_clear.py'])

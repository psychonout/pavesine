#!/usr/bin/python3
import requests
import os
import sys
import json
from os import path
from datetime import datetime, timedelta
from crontab import CronTab


PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = f'{PATH}/config.json'


def install():
    '''
        First time the script is run, this function creates the config
        file as well as cron entry for the script updating
    '''
    create_cron()
    update_config()
    return


def create_cron():
    ''' This function runs the first time and makes sure cron updates '''
    cron = CronTab(user=True)
    for item in cron:
        if 'update_cron' in item:
            break
    else:
        command = f'cd {PATH} && venv/bin/python main.py update_cron'
        job = cron.new(command=command)
        job.hour.on(0)
        job.minute.on(0)
        job.set_comment(datetime.now().date().isoformat())
        if job.is_valid():
            cron.write()
    return


def find_sockets():
    '''
        Scans the subnet and finds the Tasmota sockets
        TODO: need to use the Raspberry subnet instead of static
    '''
    sockets = []
    for i in range(255):
        try:
            url = f'http://192.168.1.{i}'
            response = requests.get(url, timeout=0.1)
            if "Tasmota" in response.text:
                sockets.append(url)
        except Exception:
            continue
    return sockets


def get_coords():
    ''' Get coordinates based on the script's IP address '''
    response = requests.get("http://ipinfo.io").json()
    lat, lon = response["loc"].split(',')
    return lat, lon


def get_timestamps(lat, lon):
    '''
        Returns a dictionary of sunrise and sunset pairs
        Returns datetime objects instead of strings
    '''
    url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}'
    response = requests.get(url).json()['results']
    timestamps = {}

    for period in ['sunrise', 'sunset']:
        ts = response[period]
        ts = datetime.strptime(ts, '%I:%M:%S %p')
        ts = ts + timedelta(hours=3)
        timestamps.update({period: ts})

    return timestamps


def update_config(force_update=True):
    '''
        If the config was updated more than week ago or if there are no sockets
        update the config.
    '''
    data = {}

    iso_date = datetime.now().date().isoformat()
    data.update({'last_update': iso_date})

    sockets = find_sockets()
    data.update({'sockets': sockets})

    lat, lon = get_coords()
    data.update({'lat': lat, 'lon': lon})

    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f)
    return data['sockets']


def get_config(force_update=False):
    '''
        Loads the data from config file, unless it doesn't exist or it's called
        by other parts of the script. (like there are no sockets to turn on)
    '''
    if force_update or not path.exists(CONFIG_PATH):
        create_cron()
        data = update_config()
    else:
        try:
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
            date_updated = datetime.strptime(data['last_update'], '%Y-%m-%d')
            week_ago = datetime.now() - timedelta(days=7)
            if (len(data['sockets']) == 0
               or (date_updated - week_ago).days == 0):
                data = update_config()
        # this is here in case there are any faults in the config file
        except Exception:
            data = update_config()
    return data['sockets'], data['lat'], data['lon']


def query(ip_address, command):
    '''
        TODO: update config if socket unreacheable to find new
        socket IP addresses
    '''
    args = f"cm?cmnd={command}"
    url = f'{ip_address}/{args}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise f"Socket returned {response.status_code}"
    except Exception:
        raise "Socket not available"


def turn_sockets(sockets, command="toggle"):
    '''
        Wrapper function that controls all sockets in the config file.
    '''
    current = 0
    while current < len(sockets):
        socket = sockets[current]
        try:
            query(socket, f'power {command}')
            current += 1
        except Exception:
            sockets = update_config(force_update=True)
            current = 0
    return True


def update_cron(timestamps):
    ''' This function gets sunrise/sunset datetimestamps and replaces
    the the necessary crontab entries'''
    cron = CronTab(user=True)
    for key in timestamps:
        hour = timestamps[key].hour
        minute = timestamps[key].minute
        job = ""
        for item in cron:
            if item.comment == key:
                job = item
                break
        else:  # if the job not found
            command = f'cd {PATH} && venv/bin/python main.py {key}'
            job = cron.new(command=command)
        job.hour.on(hour)
        job.minute.on(minute)
        job.set_comment(key)
        if job.is_valid():
            cron.write()
    for item in cron:
        if 'update_cron' in item.command:
            job = item
            job.set_comment(datetime.now().date().isoformat())
            cron.write()
            break
    return


if __name__ == "__main__":
    sockets, lat, lon = get_config()
    if len(sys.argv) == 2:
        if sys.argv[1] == "update_cron":
            update_cron(get_timestamps(lat, lon))
        else:
            if sys.argv[1] == "sunrise":
                command = 'off'
            elif sys.argv[1] == "sunset":
                command = "on"
            else:
                sys.exit()
            response = turn_sockets(sockets, command)

            if not response:
                sockets, lat, lon = install()
                turn_sockets(sockets, command)

    else:
        sys.exit("""
This program expects
    'sunrise', 'sunset' or 'update_cron' arguments.""")

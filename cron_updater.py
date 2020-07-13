#!/usr/bin/python3
import requests
import os
import sys
import json
from os import path
from datetime import datetime, timedelta
from crontab import CronTab


PY_PATH = "/usr/bin/python3"
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
    cron = CronTab(user='root')
    for item in cron:
        if 'update_cron' in item:
            break
    else:
        command = f'cd {PATH} && {PY_PATH} cron_updater.py'
        job = cron.new(command=command)
        job.hour.on(0)
        job.minute.on(0)
        job.set_comment(datetime.now().date().isoformat())
        if job.is_valid():
            cron.write()
    return


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

    lat, lon = get_coords()
    data.update({'lat': lat, 'lon': lon})

    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f)
    return data


def get_config(force_update=False):
    '''
        Loads the data from config file, unless it doesn't exist or it's called
        by other parts of the script. (like there are no sockets to turn on)
    '''
    if force_update or not path.exists(CONFIG_PATH):
        create_cron()
    data = update_config()
    return data['lat'], data['lon']


def update_cron(timestamps):
    ''' This function gets sunrise/sunset datetimestamps and replaces
    the the necessary crontab entries'''
    cron = CronTab(user='root')
    for key in timestamps:
        hour = timestamps[key].hour
        minute = timestamps[key].minute
        job = ""
        for item in cron:
            if item.comment == key:
                job = item
                break
        else:  # if the job not found
            command = f'cd {PATH} && {PY_PATH} lights_switch.py {key}'
            job = cron.new(command=command)
        job.hour.on(hour)
        job.minute.on(minute)
        job.set_comment(key)
        if job.is_valid():
            cron.write()
    for item in cron:
        if 'cron_updater' in item.command:
            job = item
            job.set_comment(datetime.now().date().isoformat())
            cron.write()
            break
    return


if __name__ == "__main__":
    lat, lon = get_config()
    update_cron(get_timestamps(lat, lon))


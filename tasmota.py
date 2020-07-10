import requests


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


def query(ip_address, command):
    '''
        TODO: update config if socket unreacheable to find new
        socket IP addresses
    '''
    args = "cm?cmnd={}".format(command)
    url = '{}/{}'.format(ip_address, args)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise "Socket returned {}".format(response.status_code)
    except Exception:
        raise "Socket not available"

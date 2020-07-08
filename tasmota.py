import requests


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

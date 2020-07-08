import requests
import time
import json
from subprocess import check_output


def alert_slack(message):
    base = "https://hooks.slack.com/services/T84M9BRTJ/"
    url = "{}B01361V6UBG/UixdwIY6dEm4AELfGng5hsgs".format(base)
    header = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url,
                                 headers=header,
                                 data=json.dumps({"text": message}))
        return response
    except Exception as e:
        print("Exception: %s", e)
        time.sleep(5)
        return alert_slack(message)


if __name__ == "__main__":
    time.sleep(60)
    name = 'Raspberry 4 - *DISCOMAN*'
    int_ip = str(check_output(['hostname', '--all-ip-addresses'])).strip()
    ext_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
    output = """
        This is {} here at KAIMAS.
        My internal IP: {}
        My external IP: {}
    """.format(name, int_ip, ext_ip)
    alert_slack(output)

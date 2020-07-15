import os
from flask import abort, request, Flask
from waitress import serve
from lights_switch import lights_in, lights_out
from datetime import datetime
# from working_dir.gsheets import add_eday_entry


def get_datetime(ts):
    date = ts.strip().split(" ")
    # May 3, 2020 at 02:28PM
    month = date[0]
    day = date[1].replace(",", "")
    if len(day) == 1:
        day = f'0{day}'
    year = date[2]
    ts_format = "%Y %B %d"
    date = f'{year} {month} {day}'
    return datetime.strptime(date, ts_format)


app = Flask(__name__)


# Main program
@app.route("/ifttt", methods=['POST'])
def main():
    # Return 408 status if the request is repeating
    if 'HTTP_X_SLACK_RETRY_NUM' in request.__dict__['environ']:
        abort(408)
    else:
        data = request.get_json()  # Event data
        print(data)
        if "status" in data:
            command = data["status"]
            if command == "on":
                lights_in()
            elif command == "off":
                lights_out()
            else:
                print(f"{command} not found")
        # elif "mirobo" in data:
            # status = data["mirobo"]
            # ip = "--ip 192.168.1.100"
            # token = "--token 34394933306855386764386c55473373"
            # os.system(f"mirobo {ip} {token} {status}")
        elif "method" in data:
            method = data["method"]
            if method == "devices":
                pass
            elif method == "finance":
                category = data["category"]
                amount = data["amount"]
                date = get_datetime(data["date"])
                date = f'{date.month}/{date.day}'
                add_eday_entry([category, "via ifttt", amount, date])
                print("Added a row in eday!")
        else:
            print(data)
    return


# Starts the bot
if __name__ == "__main__":
    port = 60000
    serve(app, host='0.0.0.0', port=port)

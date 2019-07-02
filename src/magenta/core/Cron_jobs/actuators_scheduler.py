import json
import datetime
import time
import requests
from pushbullet import Pushbullet

# TODO --- PLEASE CHANGE THIS PATH ---
SRC_PATH = "/path/here/src"

JSON_PATH = "/magenta/static/resources/json"
ENVIRONMENT_FILE = SRC_PATH + JSON_PATH + "/environment.json"
SCHEDULER_FILE = SRC_PATH + JSON_PATH + "/scheduler.json"

now = datetime.datetime.now()
dict = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}

def RelayJson(mainURL, secretKey, relay, state):
    json_value = '{"SECRET_KEY": "' + secretKey + '", "Relay":\"' + relay + '\", "Status":' + state + '}'
    MakeRequest(mainURL, json_value)
    return json_value


def MakeRequest(mainURL, json_string):
    r = requests.post(mainURL + "/sensors_actuators/setRelayStatus/", data=json_string)
    print("Request sent {0} and a response with code {1} and {2} received.".format(json, r.status_code, r.reason))


def storeJson(json_content):
    with open(SCHEDULER_FILE, 'w') as outfile:
        json.dump(json_content, outfile)


def main():
    with open(ENVIRONMENT_FILE, "r") as env_file:
        _json_environment = json.load(env_file)
        secret_key = _json_environment["key"]["security_key"]
        server_url = _json_environment["links"]["server_url"] + ":" + _json_environment["links"]["server_port"]
        pushbullet_token = _json_environment["pushbullet"]["token"]
    
    try:
        pb = Pushbullet(pushbullet_token)
    except:
        print("Error cannot connect to pushbullet with token: {0}".format(pushbullet_token))
        pb = None
    
    with open(SCHEDULER_FILE, "r") as file:
        _json_content = json.load(file)
        _system_day = dict[int((now.strftime("%w")))]
        skip_days = int(_json_content["SkipDays"])
        if ( skip_days > 0):
            skip_days -=1
            _json_content["SkipDays"] = str(skip_days)
            storeJson(_json_content)
            print("Today skipped, new remainig {0} days".format(skip_days))
            if pb is not None:
                pb.push_note("Sprinkler skip","Today skipped, new remainig {0} days".format(skip_days))
        else:
            if (_json_content["Schedule"][_system_day].lower() == "true"):
                value = int(_json_content["Duration"]["Front"])
                print ("Start Front sprinkler for {0} seconds".format(value))
                print(RelayJson(server_url, secret_key, "A", "1"))
                if pb is not None:
                    pb.push_note("Sprinkler started", "Start Front sprinkler for {0} seconds".format(value))
                time.sleep(value)
                print(RelayJson(server_url, secret_key, "A", "0"))
                if pb is not None:
                    pb.push_note("Sprinkler stopped", "Stopped Front sprinkler after {0} seconds".format(value))

                value = int(_json_content["Duration"]["Back"])
                print ("Start Back sprinkler for {0} seconds".format(value))
                print(RelayJson(server_url, secret_key, "B", "1"))
                if pb is not None:
                    pb.push_note("Sprinkler started", "Start Back sprinkler for {0} seconds".format(value))
                time.sleep(value)
                print(RelayJson(server_url, secret_key, "B", "0"))
                if pb is not None:
                    pb.push_note("Sprinkler stopped", "Stopped Back sprinkler after {0} seconds".format(value))
                
                value = int(_json_content["Duration"]["Side"])
                print ("Start Side sprinkler for {0} seconds".format(value))
                print(RelayJson(server_url, secret_key, "C", "1"))
                if pb is not None:
                    pb.push_note("Sprinkler started", "Start Side sprinkler for {0} seconds".format(value))
                time.sleep(value)
                print(RelayJson(server_url, secret_key, "C", "0"))
                if pb is not None:
                    pb.push_note("Sprinkler stopped", "Stopped Side sprinkler after {0} seconds".format(value))
                
                value = int(_json_content["Duration"]["Flowers"])
                print ("Start Flowers sprinkler for {0} seconds".format(value))
                print(RelayJson(server_url, secret_key, "D", "1"))
                if pb is not None:
                    pb.push_note("Sprinkler stopped", "Stopped Flowers sprinkler after {0} seconds".format(value))
                time.sleep(value)
                print(RelayJson(server_url, secret_key, "D", "0"))
                if pb is not None:
                    pb.push_note("Sprinkler started", "Start Flowers sprinkler for {0} seconds".format(value))
            else:
                if pb is not None:
                    pb.push_note("Sprinkler skip","Today {0}, no schedule is set. Value is set to {1}.".format(_system_day,_json_content["Schedule"][_system_day].lower()))
                print ("Today {0}, no schedule is set. Value is set to {1}.".format(_system_day,_json_content["Schedule"][_system_day].lower()))


if __name__ == "__main__":
    print("-----   start script   -----")
    main()
    print("-----   done script   -----")
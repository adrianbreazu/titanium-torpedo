import json
import datetime
import time
import requests

MAIN_PATH = "/path/here"
SECRET_KEY = "___secret_key_here______"
MAIN_URL = "http://127.0.0.1:8080"


path = MAIN_PATH + "/titanium-torpedo/src/magenta/static/resources/json/scheduler.json"
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

def RelayJson(relay, state):
    json_value = '{"SECRET_KEY": "' + SECRET_KEY + '", "Relay":\"' + relay + '\", "Status":' + state + '}'
    MakeRequest(json_value)
    return json_value


def MakeRequest(json_string):
    r = requests.post(MAIN_URL + "/sensors_actuators/setRelayStatus/", data=json_string)
    print("Request sent {0} and a response with code {1} and {2} received.".format(json, r.status_code, r.reason))


def storeJson(json_content):
    with open(path, 'w') as outfile:
        json.dump(json_content, outfile)


def main():
    with open(path, "r") as file:
        _json_content = json.load(file)
        _system_day = dict[int((now.strftime("%w")))]
        skip_days = int(_json_content["SkipDays"])
        if ( skip_days > 0):
            skip_days -=1
            _json_content["SkipDays"] = str(skip_days)
            storeJson(_json_content)
            print("One skip day passed, remainig {0} days".format(skip_days))
        else:
            if (_json_content["Schedule"][_system_day].lower() == "true"):
                value = int(_json_content["Duration"]["Front"])
                print ("Start Front sprinkler for {0} seconds".format(value))
                print(RelayJson("A", "1"))
                time.sleep(value)
                print(RelayJson("A", "0"))

                value = int(_json_content["Duration"]["Back"])
                print ("Start Back sprinkler for {0} seconds".format(value))
                print(RelayJson("B", "1"))
                time.sleep(value)
                print(RelayJson("B", "0"))
                
                value = int(_json_content["Duration"]["Side"])
                print ("Start Side sprinkler for {0} seconds".format(value))
                print(RelayJson("C", "1"))
                time.sleep(value)
                print(RelayJson("C", "0"))
                
                value = int(_json_content["Duration"]["Flowers"])
                print ("Start Flowers sprinkler for {0} seconds".format(value))
                print(RelayJson("D", "1"))
                time.sleep(value)
                print(RelayJson("D", "0"))
            else:
                print ("Today {0}, no schedule is set. Value is set to {1}.".format(_system_day,_json_content["Schedule"][_system_day].lower()))


if __name__ == "__main__":
    print("-----   start script   -----")
    main()
    print("-----   done script   -----")
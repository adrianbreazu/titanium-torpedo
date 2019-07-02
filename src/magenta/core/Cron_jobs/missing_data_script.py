import json
import requests
from pushbullet import Pushbullet

# TODO --- PLEASE CHANGE THIS PATH ---
SRC_PATH = "/path/to/src/"

JSON_PATH = "/magenta/static/resources/json"
ENVIRONMENT_FILE = SRC_PATH + JSON_PATH + "/environment.json"


def MakeRequest(mainURL):
    r = requests.post(mainURL + "/sensors_actuators/getIotReadingErrors/", data="{}")
    print("Request sent to get getIotReadingErrors and a response with code {0} and {1} received.".format(r.status_code, r.reason))
    return r.content


def main():
    with open(ENVIRONMENT_FILE, "r" ) as env_file:
        _json_environment = json.load(env_file)
        server_url = _json_environment["links"]["server_url"] + ":" + _json_environment["links"]["server_port"]
        pushbullet_token = _json_environment["pushbullet"]["token"]
    
    try:
        pb = Pushbullet(pushbullet_token)
    except:
        print("Error cannot connect to pushbullet with token: {0}".format(pushbullet_token))
        pb = None
    
    if (pb is not None):
        respone_json = MakeRequest(server_url)
        #print("Response received : {0}".format(respone_json))
        sensor_string = json.loads(respone_json.decode('utf-8'))
        sensors_error_list = sensor_string["response"]
        #print("error list {0}".format(sensors_error_list))
        if len(sensors_error_list) > 0:
            pb.push_note("Sensors read error", "The following sensors are not sendind data for more than 1 hour: {0}. Please take a look!".format(",".join(sensors_error_list)))
        else:
            print("Everything is ok, the list is empty.")


if __name__ == "__main__":
    main()
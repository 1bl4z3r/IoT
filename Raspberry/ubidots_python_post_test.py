import time
import requests
import math
import random

TOKEN = ""  # Put your TOKEN here
DEVICE_LABEL = "Device1"  # Put your device label here 
VARIABLE_LABEL_1 = "Current"  # Put your first variable label here
VARIABLE_LABEL_2 = "Voltage"  # Put your second variable label here


def build_payload(variable_1, variable_2):
    value_1 = random.randint(14, 16)
    value_2 = random.randint(190, 220)
    payload = {variable_1: value_1,variable_2: value_2}
    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    #url = "http://things.ubidots.com"
    url = "http://things.ubidots.com/api/v1.6/devices/{}".format(DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False
    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2)
    print("[INFO] Attemping to send data {}".format(payload))
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(5)
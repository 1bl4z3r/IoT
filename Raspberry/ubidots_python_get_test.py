import requests
import random
import time

TOKEN = "" # Assign your Ubidots Token
DEVICE = "Device1" # Assign the device label to obtain the variable
VARIABLE = "Fan" # Assign the variable label to obtain the variable value
DELAY = 1  # Delay in seconds

def get_var(device, variable):
    try:
        url = "http://things.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except:
        pass


if __name__ == "__main__":
    while True:
        print(get_var(DEVICE, VARIABLE))
        time.sleep(DELAY)

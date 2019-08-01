import requests
import random
import time
import RPi.GPIO as GPIO

TOKEN = "" # Assign your Ubidots Token
DEVICE = "rpi" # Assign the device label to obtain the variable
VARIABLE = "fan_logic" # Assign the variable label to obtain the variable value
DELAY = 1  # Delay in seconds
fl=0

GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output

def get_var(device, variable):
    try:
        url = "http://things.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
        GPIO.cleanup()                 # resets all GPIO ports used by this program
    


if __name__ == "__main__":
    while True:
        fl=int(get_var(DEVICE, VARIABLE))
        print (fl)
        if fl==1:
            GPIO.output(24, 1)                 # set GPIO24 to 1/GPIO.HIGH/True
            print ("Fan is on")
        elif fl==2:
            GPIO.output(24, 1)                # set GPIO24 to 1/GPIO.HIGH/True
            print ("Fan is Override on")
        else:
            GPIO.output(24, 0)             # set GPIO24 to 0/GPIO.LOW/False
            print ("Fan is Off")
        time.sleep(DELAY)

  

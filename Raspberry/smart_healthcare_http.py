import RPi.GPIO as GPIO
import grovepi
import math
import requests,json
import time
import smbus
import serial
import time

# Connect the Grove Temperature Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0
grovepi.pinMode(sensor,"INPUT")
# Connect the Grove Gas Sensor to analog port A1
# SIG,NC,VCC,GND
gas_sensor = 1
grovepi.pinMode(gas_sensor,"INPUT")

# Connect the Grove Touch Sensor to digital port D5
# SIG,NC,VCC,GND
touch_sensor = 5
grovepi.pinMode(touch_sensor,"INPUT")
##

grovepi.pinMode(gas_sensor,"INPUT")
##
#Fire Flame Sensor GPIO SETUP
flame_sensor = 6
grovepi.pinMode(flame_sensor,"INPUT")

##serialCommunication with arduino
ser= serial.Serial('/dev/ttyACM0',115200)

url ="http://162.255.85.191:8080/device/smart-health-care-system?id=5b6dcad7924060685e9c6eae"

def send_to_cloud(x1, y1, temp, gas, touch, flame):
    data = json.dumps([{"sensor" : "temperature", "value":temp, "timestamp":"","context":"Temperature:Celsius"},
                       {"sensor": "gas",  "value":gas, "timestamp":"","context":"Gas:PPM"},
                       {"sensor": "touch",  "value":touch, "timestamp":"","context":"Touch:No|Yes"},
                       {"sensor": "pulse-sensor",  "value":y1, "timestamp":"Pulse:PPM","context":"Pulse:PPM"},
                       {"sensor": "flame",  "value":flame, "timestamp":"","context":"Flame:No|Yes"}, 
                       {"sensor": "co2",  "value":x1, "timestamp":"","context":"Co2:PPM"}])

    r = requests.post(url,data)
    print(r.text)   
            
    return

while True:
    try:
        #serial communication with Arduino
        s = str(ser.readline())
        x=s.split("|")[0]
        x1=x.split("'")[1]
        y=s.split("|")[1]
        y1=y.split("\\")[0]
        print("")
        print("Co2 = ",x1,"PPM")
        print("---------------------")
        print("")
        print("Pulse = ",y1,"BPM")
        print("---------------------")
        print("")

            

##
        #Flame Sensor
        flame = grovepi.digitalRead(flame_sensor)
        if flame==0 or flame==1:	
            if flame==0:
                print ('Flame Detected')
                print("----------------")
                print("")

            else:
                print ('Flame Not Detected')
                print("----------------")
                print("")

    	# This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        temp = grovepi.temp(sensor,'1.1')
        print("Temperature =", temp,"C")
        print("----------------")
        print("")



        # Get touch sensor value
        touch = grovepi.digitalRead(touch_sensor)
        if touch==0 or touch==1:	
            if touch==1:
                print ('Touch Detected')
                print("---------------------")
                print("")
            else:
                print ('Touch Not Detected')
                print("---------------------")
                print("")
##

##
        # Get gas sensor value
        gas = grovepi.analogRead(gas_sensor)
        # Calculate gas density - large value means more dense gas
        density = (float)(gas / 1024)
        print("Gas Sensor Value=", gas, " Density =", density)
        print("----------------------------------------------")
        print("")
        
        send_to_cloud(x1, y1, temp, gas, touch, flame)
        time.sleep(1)

    except IOError:
        print ("Error")

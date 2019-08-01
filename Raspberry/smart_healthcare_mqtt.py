#!/usr/bin/python
import RPi.GPIO as GPIO
import grovepi
import math
import requests,json
import time
import smbus
import serial
import time
import paho.mqtt.client as mqtt




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

Broker = "59.162.178.178"
port = 1883

client = mqtt.Client()

client.connect(Broker,port)

topic = "device/5b95148d5c89ef2b048388e4"
print("------------------------------------------")
print("------------------------------------------")
print(" ")
print("HEALTHCARE MONITORING SYSTEM ")
print(" ")
print("------------------------------------------")
print("------------------------------------------")
while True:
    try:
        #serial communication with Arduino
        print ('Scanning sensors ....')
        print("------------------------------------------")
        s = str(ser.readline())
        x=s.split("|")[0]
        x1=x.split("'")[1]
        y=s.split("|")[1]
        y1=y.split("\\")[0]
        print("")
        print("CO2    : ",x1,"PPM")
        print("----------------------------------------------")
        print("")
        print("Pulse  : ",y1,"BPM")
        print("----------------------------------------------")
        print("")

            

##
        #Flame Sensor
        flame = grovepi.digitalRead(flame_sensor)
        if flame==0 or flame==1:	
            if flame==0:
                print ('Flame : Detected')
                print("----------------------------------------------")
                print("")

            else:
                print ('Flame : Not Detected')
                print("----------------------------------------------")
                print("")

    	# This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        temp = grovepi.temp(sensor,'1.1')
        print("Temperature : ", round(temp,2)," Degree Celcius")
        print("----------------------------------------------")
        print("")



        # Get touch sensor value
        touch = grovepi.digitalRead(touch_sensor)
        if touch==0 or touch==1:	
            if touch==1:
                print ('Touch : Not Detected')
                print("----------------------------------------------")
                print("")
            else:
                print ('Touch : Detected')
                print("----------------------------------------------")
                print("")
##

##
        # Get gas sensor value
        gas = grovepi.analogRead(gas_sensor)
        # Calculate gas density - large value means more dense gas
        density = (float)(gas / 1024)
        print("Gas Sensor Value : ", gas, "PPM, Density : ", round(density,2))
        print("----------------------------------------------")
        print("")
        data = json.dumps([{"sensor" : "temperature", "value":temp, "timestamp":"","context":"Temperature:Celsius"},
                       {"sensor": "gas",  "value":gas, "timestamp":"","context":"Gas:PPM"},
                       {"sensor": "touch",  "value":touch, "timestamp":"","context":"Touch:No|Yes"},
                       {"sensor": "pulse-sensor",  "value":y1, "timestamp":"Pulse:PPM","context":"Pulse:PPM"},
                       {"sensor": "flame",  "value":flame, "timestamp":"","context":"Flame:No|Yes"}, 
                       {"sensor": "co2",  "value":x1, "timestamp":"","context":"Co2:PPM"}])
        
        print("")
        client.publish(topic,data)
        
        print("------------------------------------------")
        print("------------------------------------------")
        print(" ")
        print("Data uploaded ")
        print(" ")
        print("------------------------------------------")
        print("------------------------------------------")
        time.sleep(5)

    except IOError:
        print ("Error")

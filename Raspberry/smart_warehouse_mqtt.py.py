

                                                                                         

#!/usr/bin/env python
#
# GrovePi Example for using the Grove Ultrasonic Ranger (http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import grovepi
import RPi.GPIO as GPIO
import time
import math
import requests, json
import smbus
import math
import urllib
import pprint
import serial
from picamera import PiCamera
import paho.mqtt.client as mqtt
# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 2

# Connect the LED to digital port D4
# SIG,NC,VCC,GND
led = 4

# Turn on LED once sensor exceeds threshold resistance
threshold = 10

sensor = 6  # The Temperatur And Humiduty Sensor goes on digital port 6 D6.

magnetic_switch = 5 #Sensor goes on digital port 5 D5.

#motion=0
#Fire Flame Sensor
channel =1  #Sensor goes on digital port 1 D1.

# Connect the Grove Gas Sensor MQ2 to analog port A1
# SIG,NC,VCC,GND
gas_sensor1 = 0

grovepi.pinMode(gas_sensor1,"INPUT")

# Connect the Grove Gas Sensor MQ 8 to analog port A2
# SIG,NC,VCC,GND
gas_sensor2 = 1

Broker ="59.162.178.178"
port = 1883

client = mqtt.Client()
client.connect(Broker,port)

grovepi.pinMode(gas_sensor2,"INPUT")

#serialCommunication with arduino
ser= serial.Serial('/dev/ttyACM0',115200)

#3-Axis Accelerometer Sensor
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

camera = PiCamera() 
camera.rotation = 180
#camera.start_preview()
#time.sleep(1)

 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect

# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)




#temp_humidity_sensor_type
#Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

grovepi.pinMode(sensor,"INPUT")

grovepi.pinMode(magnetic_switch,"INPUT")

grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")



topic = "device/5b9511315c89ef2b04838892"

print("-----------------------------------")
print("-----------------------------------")
print(" ")
print(" ")
print("SMART MANUFACTURING & WAREHOUSE SYSTEM")
print(" ")
print(" ")
print("-----------------------------------")
print("-----------------------------------")


            

while True:
    try:

        #serial communication with Arduino
        print(" ")
        print(" ")
        print("Started scanning Sensors...........")
        print("-----------------------------------")
        s = str(ser.readline())
        x=s.split("|")[0]
        x1=x.split("'")[1]
        y=s.split("|")[1]
        z=s.split("|")[2]
        z1=z.split("\\")[0]
        print("Dust : ",x1)
        print("---------------------")
        print("")
        print("Co2  : ",y)
        print("---------------------")
        print("")
        print("RMS Current :  ",z1)
        print("---------------------")
        print("")
        # Get sensor value
        sensor_value1 = grovepi.analogRead(gas_sensor1)
        # Calculate gas density - large value means more dense gas
        density = (float)(sensor_value1/1024)
        print("Gas Sensor :", sensor_value1, " GAS Density :", round(density,2))
        print("---------------------")
        print("")
        
        # Get sensor value
        sensor_value2 = grovepi.analogRead(gas_sensor2)

        # Calculate gas density - large value means more dense gas
        density1 = (float)(sensor_value2 / 1024)

        print("Hydrogen Gas : ", sensor_value2, " Hydrogen Gas Density =", round(density1,2))
        print("---------------------")
        print("")

        # Get sensor value
        light = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        resistance = round(((float)(1023 - light) * 10 / light),2)

        if resistance > threshold:
            # Send HIGH to switch on LED
            grovepi.digitalWrite(led,1)
        else:
            # Send LOW to switch off LED
            grovepi.digitalWrite(led,0)

        print("Light Intensity  : %d Resistance : %.2f" %(round(light,2) ,round(resistance,2)))
        print("---------------------")
        print("")
        #Fire Flame Snesor
        fire = grovepi.digitalRead(channel)
        if fire==0 or fire==1:	
            if fire==1:
                print ('Flame : Not Detected')
            else:
                print ('Flame : Detected')
       
        print("---------------------")
        print("")
        #print("magnetic switch detected")
        
        
        magnetic = grovepi.digitalRead(magnetic_switch)
        if magnetic==0 or magnetic==1:	
            if magnetic==1:
                print ('Magnet : Detected')
                camera.capture('/home/pi/Desktop/image/'+ str(time.time())+'.jpg')
                print("Camera Captured")
                #print("---------------------")
                #print("")
                camera.stop_preview()
            else:
                print ('Magnet : Not detected')
        print("---------------------")
        print("")
        
        
        # This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp,humidity] = grovepi.dht(sensor,white)  
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            #print("Temparature and Humidity sensor value")
            print("Temparature = %.02f C"%(temp))
            print("--------")
            print("")
            print("Humidity = %.02f%%"%(humidity))
            print("--------")
            print("")

        #3-Axis Accelerometer Snesor
        print("Gyroscope Values")
        print("--------")
        Gyroscop_xout = read_word_2c(0x43)
        Gyroscop_yout = read_word_2c(0x45)
        Gyroscop_zout = read_word_2c(0x47)
       
        print(("Gyroscope_x_axis: "), ("%5d" % Gyroscop_xout), (" Scaled: "), round((Gyroscop_xout / 131),2))
        print(("Gyroscope_y_axis: "), ("%5d" % Gyroscop_yout), (" Scaled: "), round((Gyroscop_yout / 131),2))
        print(("Gyroscope_z_axis: "), ("%5d" % Gyroscop_zout), (" Scaled: "), round((Gyroscop_zout / 131),2)) 
        print()
        print("Acceleration Values")
        print("---------------------")
        acceleration_xout = read_word_2c(0x3b)
        acceleration_yout = read_word_2c(0x3d)
        acceleration_zout = read_word_2c(0x3f)
         
        acceleration_xout_scaled = acceleration_xout / 16384.0
        acceleration_yout_scaled = acceleration_yout / 16384.0
        acceleration_zout_scaled = acceleration_zout / 16384.0
         
        
        print ("Acceleration_x_axis: ", ("%6d" % acceleration_xout), (" Scaled: "), round(acceleration_xout_scaled,2))
        print ("Acceleration_y_axis: ", ("%6d" % acceleration_yout), (" Scaled: "), round(acceleration_yout_scaled,2))
        print ("Acceleration_z_axis: ", ("%6d" % acceleration_zout), (" Scaled: "), round(acceleration_zout_scaled,2))
        print()
        print("Rotation Values")
        print("---------")
        x_rotation = get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        y_rotation = get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        print("Rotation of x-axis : ",round(x_rotation,2))     
        print("Rotation of y-axis : ",round(y_rotation,2))
        print("---------------------")
        print("")
        #time.sleep(10)
        data = json.dumps([{"sensor" : "light-sensor", "value":light, "timestamp":"", "context":"light sensor!!"},
            {"sensor": "hydrogen-gas-sensor",  "value":density1, "timestamp":"", "context":"Hydrogen gas"},
            {"sensor": "gas-sensor",  "value":density, "timestamp":"", "context":"Gas sensor"},
            {"sensor": "fire-flame-sensor",  "value":fire, "timestamp":"", "context":"Flame Sensor"},
            {"sensor": "temperature",  "value":temp, "timestamp":"", "context":"Temperature"},
            {"sensor": "humidity",  "value":humidity, "timestamp":"", "context":"Hunidity"},
            {"sensor": "magnetic-switch",  "value":magnetic, "timestamp":"", "context":"Magnetic Switch!!"},
            {"sensor": "dust-sensor",  "value":x1, "timestamp":"", "context":"Dust Density"},
            {"sensor": "co2-sensor",  "value":y, "timestamp":"", "context":"Co2 Level"},
            {"sensor": "current-sensor",  "value":z1, "timestamp":"", "context":"RMS Current"},
            {"sensor": "accelerometer-x",  "value":(acceleration_xout), "timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "accelerometer-y",  "value":(acceleration_yout), "timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "accelerometer-z",  "value":(acceleration_zout), "timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "gyroscope-x",  "value":(Gyroscop_xout), "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "gyroscope-y",  "value":(Gyroscop_yout), "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "gyroscope-z",  "value":(Gyroscop_zout), "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "rotation-x",  "value":(x_rotation), "timestamp":"", "context":"Rotation(x,y)"},
            {"sensor": "rotation-y",  "value":(y_rotation), "timestamp":"", "context":"Rotation(x,y)"}])
        client.publish(topic,data)
        print("-----------------------------------")
        print("-----------------------------------")
        print(" ")
        print(" ")
        print("Data uploaded")
        print(" ")
        print(" ")
        print("-----------------------------------")
        print("-----------------------------------")
        
        time.sleep(5)
        
    
    except TypeError:
        print ("type error")
    except IOError:
        print ("IO Error")

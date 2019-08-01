import grovepi
import RPi.GPIO as GPIO
import time
import math
import requests, json
import smbus
import math
import urllib
import pprint
import paho.mqtt.client as mqtt

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

sensor = 7  # The Temperatur And Humiduty Sensor goes on digital port 2.
pir_sensor = 8
magnetic_switch = 0
Broker = "59.162.178.178"
port = 1883

motion=0
#Fire Flame Sensor
channel = 2
#IR Sensor
ir= 5
#Ultrasonic Sensor
ultrasonic_ranger = 6
#3-Axis Accelerometer Sensor
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
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

bus.write_byte_data(address, power_mgmt_1, 0)




# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.




grovepi.pinMode(pir_sensor,"INPUT")

grovepi.pinMode(magnetic_switch,"INPUT")
grovepi.pinMode(channel,"INPUT")
grovepi.pinMode(ir,"INPUT")
grovepi.pinMode(sensor,"INPUT")

client = mqtt.Client()

client.connect(Broker,port)

topic = "device/5b950d255c89ef2b0483886c"

print("-----------------------------------------------------------")
print("-----------------------------------------------------------")
print(" ")
print(" ")
print("SMART AUTOMOBILE SYSTEM")
print(" ")
print(" ")
print("------------------------------------------------------------")
print("------------------------------------------------------------")
print(" ")
print(" ")

while True:
    try:
        #IR Snesor
        print("--------------------")
        print("Start scanning sensors.........")

        
              
        print("---------------------")
        print()
        obj = grovepi.digitalRead(ir)
        if obj==0 or obj==1:	
            if obj==0:
                print ('IR : Object Detected')
            else:
                print ('IR : Object Not Detected')
        print("---------------------")
        print()
        
        #Fire Flame Snesor
        
        fire = grovepi.digitalRead(channel)
        if fire==0 or fire==1:	
            if fire==0:
                print ('Flame : Detected')
            else:
                print ('Flame : Not Detected')
        print("---------------------")
        print()
        
        #print("magnetic switch detected")
        
        magnetic = grovepi.digitalRead(magnetic_switch)
        if magnetic==0 or magnetic==1:	
            if magnetic==1:
                print ('Magnet : Detected')
            else:
                print ('Magnet : Not Detected')
        print("---------------------")
        print()
        
        motion = grovepi.digitalRead(pir_sensor)
        # check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
        if motion==0 or motion==1:	
            if motion==1:
                print ('PIR Motion : Detected')
            else:
                print ('PIR Motion : Not Detected')
        print("---------------------")
        print()
        
##        # Read distance value from Ultrasonic
        # Read distance value from Ultrasonic
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)
        print("Ultrasonic : ",distance," cm")
        print("----------------------")   
        # Reset by pressing CTRL + C
        
        # This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp,humidity] = grovepi.dht(sensor,white)  
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            #print("Temparature and Humidity sensor value")
            print()
            print("Temperature : %.02f C"%(temp))
            print("--------------------")
            print()
            print("Humidity    : %.02f%%"%(humidity))
            print("--------------------")

        #3-Axis Accelerometer Snesor
        print()
        print("Gyroscope Values")
        print("------------------------")
        Gyroscop_xout = read_word_2c(0x43)
        Gyroscop_yout = read_word_2c(0x45)
        Gyroscop_zout = read_word_2c(0x47)
       
        print(("Gyroscope_x_axis: "), ("%5d" % Gyroscop_xout), (" Scaled: "), (round((Gyroscop_xout / 131),2)))
        print(("Gyroscope_y_axis: "), ("%5d" % Gyroscop_yout), (" Scaled: "), (round((Gyroscop_yout / 131),2)))
        print(("Gyroscope_z_axis: "), ("%5d" % Gyroscop_zout), (" Scaled: "), (round((Gyroscop_zout / 131),2))) 
        print()
        print("Acceleration values")
        print("-----------------------")
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
        print("Rotation values")
        print("------------------------")
        x_rotation = get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        y_rotation = get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        print("Rotation of x_axis: ",round(x_rotation,2))     
        print("Rotation of y_axis: ",round(y_rotation,2))
        print("------------------------")
        print("")
        data=json.dumps([{"sensor" : "humidity", "value":humidity,"timestamp":"", "context":"temparature sensor!!"},
            {"sensor": "temperature",  "value":temp, "timestamp":"", "context":"Humidity!!"},
            {"sensor": "ultrasonic-sensor",  "value":distance, "timestamp":"", "context":"Ultrasonic sensor!"},
            {"sensor": "pir-motion-sensor",  "value":motion, "timestamp":"", "context":"Pir motion sensor!"},
            {"sensor": "fire-flame-sensor",  "value":fire, "timestamp":"", "context":"Fire Flame!"},
            {"sensor": "magnetic-switch",  "value":magnetic, "timestamp":"", "context":"Magnetic Switch!!"},
            {"sensor": "accelerometer-x",  "value":acceleration_xout,"timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "accelerometer-y",  "value":acceleration_yout,"timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "accelerometer-z",  "value":acceleration_zout,"timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "gyroscope-x",  "value":Gyroscop_xout, "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "gyroscope-y",  "value":Gyroscop_yout, "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "gyroscope-z",  "value":Gyroscop_zout, "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "rotation-x",  "value":x_rotation,"timestamp":"", "context":"Rotation(x,y)"},
            {"sensor": "rotation-y",  "value":y_rotation,"timestamp":"", "context":"Rotation(x,y)"},            
            {"sensor": "ir-sensor",  "value":obj, "timestamp":"", "context":"Object(0(Not Detected)/1(Detected))"}])

        client.publish(topic,data)
        print("-----------------------------------------------------------")
        print("-----------------------------------------------------------")
        print(" ")
        print(" ")
        print("Data uploaded")
        print(" ")
        print(" ")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print(" ")
        print(" ")
        print(" ")
        time.sleep(5)
##        
    except TypeError:
        print ("type error")
    except IOError:
        print ("IO Error")
        time.sleep(10)

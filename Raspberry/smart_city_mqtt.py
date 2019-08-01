import grovepi
import time
import math
import requests, json
import RPi.GPIO as GPIO
from picamera import PiCamera
import serial
import smbus
import math
import SimpleMFRC522
import paho.mqtt.client as mqtt

# Connect the Grove Ultrasonic Ranger to digital port D6
# SIG,NC,VCC,GND 
ultrasonic_ranger = 6
# Connect the Grove PIR Motion Sensor to digital port D8
pir_sensor = 8
# Connect the Grove Magnetic Switch Sensor to digital port D7
magnetic_switch = 7
#sound sensor  digital port A0
sound_sensor = 0

#Ultrasonic Range Sensor
grovepi.pinMode(ultrasonic_ranger,"INPUT")
#Pir Motion Sensor
motion=0
grovepi.pinMode(pir_sensor,"INPUT")

#serialCommunication with arduino
#ser= serial.Serial('/dev/ttyACM0',115200)


# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

grovepi.pinMode(magnetic_switch,"INPUT")


reader = SimpleMFRC522.SimpleMFRC522()


#IR Analog Sensor

IR =5  #Sensor goes on digital port 5 D5 Sound

#Fire Flame Sensor
channel =2 #Sensor goes on digital port 2 D2.

#3-Axis Accelerometer Sensor
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

camera = PiCamera()
grovepi.pinMode(sound_sensor,"INPUT")

Broker = "59.162.178.178"
port = 1883

client = mqtt.Client()
client.connect(Broker,port)



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
address = 0x68   # via i2cdetect

threshold_value = 200

bus.write_byte_data(address, power_mgmt_1, 0)
         
        

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0]

topic = "device/5b950bc75c89ef2b04838861"

print("----------------------------------------------------")
print("----------------------------------------------------")
print(" ")
print(" ")
print("SMART CITY SYSTEM")
print(" ")
print(" ")
print("----------------------------------------------------")
print("----------------------------------------------------")

while True:
    try:
        
        print(" ")
        print("Started scanning sensors")
        print(" ")
        print("----------------------------------------------------")
        #serial communication with Arduino
        s = str(ser.readline())
        x=s.split("|")[0]
        alcohol=x.split("'")[1]
        dust=s.split("|")[1]
        z=s.split("|")[2]
        rms_current=z.split("\\")[0]
        print("")
        print("Dust        : ",dust)
        print("---------------------")
        print("")
        print("Alcohol      : ",alcohol)
        print("---------------------")
        print("")
        print("RMS Current  :",rms_current)
        print("---------------------")
        print("")

        #3-Axis Accelerometer Snesor
        print("Gyroscope")
        print("---------------------------------")
        Gyroscop_xout = read_word_2c(0x43)
        Gyroscop_yout = read_word_2c(0x45)
        Gyroscop_zout = read_word_2c(0x47)
       
        print(("Gyroscope_xaxis : "), ("%5d" % Gyroscop_xout), (" scaled: "), (round((Gyroscop_xout / 131),2)))
        print(("Gyroscope_yaxis : "), ("%5d" % Gyroscop_yout), (" scaled: "), (round((Gyroscop_yout / 131),2)))
        print(("Gyroscope_zaxis : "), ("%5d" % Gyroscop_zout), (" scaled: "), (round((Gyroscop_zout / 131),2))) 
        print()
        print("Acceleration sensor")
        print("--------------------------------")
        acceleration_xout = read_word_2c(0x3b)
        acceleration_yout = read_word_2c(0x3d)
        acceleration_zout = read_word_2c(0x3f)
         
        acceleration_xout_scaled = acceleration_xout / 16384.0
        acceleration_yout_scaled = acceleration_yout / 16384.0
        acceleration_zout_scaled = acceleration_zout / 16384.0
         
        
        print ("Acceleration_xaxis: ", ("%6d" % acceleration_xout), (" scaled: "), round(acceleration_xout_scaled,2))
        print ("Acceleration_yaxis: ", ("%6d" % acceleration_yout), (" scaled: "), round(acceleration_yout_scaled,2))
        print ("Acceleration_zaxis: ", ("%6d" % acceleration_zout), (" scaled: "), round(acceleration_zout_scaled,2))
        print()
        print("Rotation")
        print("---------------------------------")
        x_rotation = get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        y_rotation = get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        print("X Rotation values : ",round(x_rotation),2)     
        print("Y Rotation values : ",round(y_rotation),2)
        print("---------------------------------")
        print(" ")

        
        #print("magnetic switch detected")
        magnetic = grovepi.digitalRead(magnetic_switch)
        if magnetic==0 or magnetic==1:	
            if magnetic==1:
                
                camera.rotation = 180
                camera.start_preview()
                ##CAmera

                camera.capture('/home/pi/Desktop/images/'+ str(time.time())+'.jpg')
                print("Camera Captured")
                print("---------------------")
                print("")
                camera.stop_preview()
                print ('Magnet :  Detected')
                print("---------------------")
                print("")
            else:
                print ('Magnet : Not Detected')
                print("---------------------")
                print("")

 
        
        motion = grovepi.digitalRead(pir_sensor)
        # check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
        if motion==0 or motion==1:	
            if motion==1:
                print ('Motion : Detected')
                print("----------------")
                print("")
            else:
                print ('Motion : Not detected')
                print("----------------")
                print("")
        

        # Read distance value from Ultrasonic
        
        ultra_sonic=grovepi.ultrasonicRead(ultrasonic_ranger)
        print("Ultra-sonic : ",ultra_sonic)
        print("---------------------")
        print("")

        
        
        
        # Read the sound level
        sensor_value = grovepi.analogRead(sound_sensor)
        print("Sound Level : ",sensor_value)
        print("----------------")
        print("")

        

        ##IR Sensor
        
        ir_sensor = grovepi.digitalRead(IR)
        if ir_sensor==0 or ir_sensor==1:	
            if ir_sensor==0:
                print ('IR Object : Detected')
            else:
                print ('IR Object : Not Detected')
       
        print("---------------------")
        print("")
            
        
        #Fire Flame Snesor
        fire = grovepi.digitalRead(channel)
        if fire==0 or fire==1:	
            if fire==0:
                print ('Flame : Detected')
            else:
                print ('Flame : Not Detected')
       
        print("---------------------")
        print("")
            
##        RFID reader
        
        id, text = reader.read()
        print("RFID id   : ", id)
        print("RFID Data : ", text)
        print("---------------------")
        print("---------------------")
        print("")
        data = json.dumps([
            {"sensor": "optical-dust-sensor",  "value":dust, "timestamp":"", "context":"Dust sensor!"},
            {"sensor": "alcohol-gas-sensor",  "value":alcohol, "timestamp":"", "context":"Alcohol sensor!"},
            {"sensor": "current-sensor",  "value":rms_current, "timestamp":"", "context":"RMS Current!!"},
            {"sensor": "magnetic-switch",  "value":magnetic, "timestamp":"", "context":"Magnetic Switch!!"},
            {"sensor": "pir-motion-sensor",  "value":motion, "timestamp":"", "context":"Motion Sensor!!"},
            {"sensor": "sound-sensor",  "value":sensor_value, "timestamp":"", "context":"Sound sensor!"},
            {"sensor": "ultrasonic-sensor",  "value":ultra_sonic, "timestamp":"", "context":"ultra sonic sensor!!"},
            {"sensor": "ir-sensor",  "value":ir_sensor, "timestamp":"", "context":"accelerometer sensor!!"},
            {"sensor": "fire-flame-sensor",  "value":fire, "timestamp":"", "context":"Flame Value!!"},
            {"sensor": "rfid-reader",  "value":id, "timestamp":"", "context":"Flame Value!!"},
            {"sensor": "accelerometer-x",  "value":acceleration_xout,"timestamp":"", "context":"Acceleration (x)"},
            {"sensor": "accelerometer-y",  "value":acceleration_yout,"timestamp":"", "context":"Acceleration (y)"},
            {"sensor": "accelerometer-z",  "value":acceleration_zout,"timestamp":"", "context":"Acceleration (z)"},
            {"sensor": "gyroscope-x",  "value":Gyroscop_xout, "timestamp":"", "context":"Gyro (x)"},
            {"sensor": "gyroscope-y",  "value":Gyroscop_yout, "timestamp":"", "context":"Gyro (y)"},
            {"sensor": "gyroscope-z",  "value":Gyroscop_zout, "timestamp":"", "context":"Gyro (z)"},
            {"sensor": "rotation-x",  "value":x_rotation,"timestamp":"", "context":"Rotation(x)"},
            {"sensor": "rotation-y",  "value":y_rotation,"timestamp":"", "context":"Rotation(y)"}])
            
      
        client.publish(topic,data)
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print(" ")
        print(" ")
        print("Data uploaded")
        print(" ")
        print(" ")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        
        time.sleep(5)

        
    except TypeError:
        print ("type error")
    except IOError:
        print ("IO Error")

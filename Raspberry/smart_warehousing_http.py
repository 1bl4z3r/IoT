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



url = "http://162.255.85.191:8080/device/smart-warehouse?id=5b67d6af924060685e9c6d93"

def send_to_cloud(x1,y,z1,density,density1,light,fire,temp,humidity,magnetic,acceleration_xout,acceleration_yout,acceleration_zout,Gyroscop_xout,Gyroscop_yout,Gyroscop_zout,x_rotation,y_rotation):
            data = json.dumps([{"sensor" : "light-sensor", "value":light, "timestamp":"", "context":"light sensor!!"},
            {"sensor": "hydrogen-gas-sensor",  "value":density1, "timestamp":"", "context":"Hydrogen gas"},
            {"sensor": "gas-sensor",  "value":density, "timestamp":"", "context":"Gas sensor"},
            {"sensor": "flame-sensor",  "value":fire, "timestamp":"", "context":"Flame Sensor"},
            {"sensor": "temperature",  "value":temp, "timestamp":"", "context":"Temperature"},
            {"sensor": "humidity",  "value":humidity, "timestamp":"", "context":"Hunidity"},
            {"sensor": "magnetic-switch",  "value":magnetic, "timestamp":"", "context":"Magnetic Switch!!"},
            {"sensor": "dust-sensor",  "value":x1, "timestamp":"", "context":"Dust Density"},
            {"sensor": "co2-sensor",  "value":y, "timestamp":"", "context":"Co2 Level"},
            {"sensor": "current-sensor",  "value":z1, "timestamp":"", "context":"RMS Current"},
            {"sensor": "accelerometer",  "value":(acceleration_xout), "timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "accelerometer",  "value":(acceleration_yout), "timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "accelerometer",  "value":(acceleration_zout), "timestamp":"", "context":"Acceleration (x,y,z)"},
            {"sensor": "gyroscope",  "value":(Gyroscop_xout), "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "gyroscope",  "value":(Gyroscop_yout), "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "gyroscope",  "value":(Gyroscop_zout), "timestamp":"", "context":"Gyro (x,y,z)"},
            {"sensor": "rotation",  "value":(x_rotation), "timestamp":"", "context":"Rotation(x,y)"},
            {"sensor": "rotation",  "value":(y_rotation), "timestamp":"", "context":"Rotation(x,y)"}])

            r=requests.post(url,data)
            print(r.text)   
            
            return

while True:
    try:

        #serial communication with Arduino
        s = str(ser.readline())
        x=s.split("|")[0]
        x1=x.split("'")[1]
        y=s.split("|")[1]
        z=s.split("|")[2]
        z1=z.split("\\")[0]
        print("Dust = ",x1)
        print("---------------------")
        print("")
        print("Co2 = ",y)
        print("---------------------")
        print("")
        print("RMS Current= ",z1)
        print("---------------------")
        print("")
        # Get sensor value
        sensor_value1 = grovepi.analogRead(gas_sensor1)
        # Calculate gas density - large value means more dense gas
        density = (float)(sensor_value1/1024)
        print("Gas Sensor =", sensor_value1, " Density =", density)
        print("---------------------")
        print("")
        
        # Get sensor value
        sensor_value2 = grovepi.analogRead(gas_sensor2)

        # Calculate gas density - large value means more dense gas
        density1 = (float)(sensor_value2 / 1024)

        print("Hydrogen Gas =", sensor_value2, " Density =", density1)
        print("---------------------")
        print("")

        # Get sensor value
        light = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        resistance = (float)(1023 - light) * 10 / light

        if resistance > threshold:
            # Send HIGH to switch on LED
            grovepi.digitalWrite(led,1)
        else:
            # Send LOW to switch off LED
            grovepi.digitalWrite(led,0)

        print("Light Intencity = %d Resistance = %.2f" %(light,  resistance))
        print("---------------------")
        print("")
        #Fire Flame Snesor
        fire = grovepi.digitalRead(channel)
        if fire==0 or fire==1:	
            if fire==1:
                print ('Flame Not Detected')
            else:
                print ('Flame Detected')
       
        print("---------------------")
        print("")
        #print("magnetic switch detected")
        
        
        magnetic = grovepi.digitalRead(magnetic_switch)
        if magnetic==0 or magnetic==1:	
            if magnetic==1:
                print ('Magnet Detected')
                camera.capture('/home/pi/Desktop/image/'+ str(time.time())+'.jpg')
                print("Camera Captured")
                print("---------------------")
                print("")
                camera.stop_preview()
            else:
                print ('Magnet not detected')
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
        print("Gyroscop")
        print("--------")
        Gyroscop_xout = read_word_2c(0x43)
        Gyroscop_yout = read_word_2c(0x45)
        Gyroscop_zout = read_word_2c(0x47)
       
        print(("Gyroscop_xout: "), ("%5d" % Gyroscop_xout), (" scaled: "), (Gyroscop_xout / 131))
        print(("Gyroscop_yout: "), ("%5d" % Gyroscop_yout), (" scaled: "), (Gyroscop_yout / 131))
        print(("Gyroscop_zout: "), ("%5d" % Gyroscop_zout), (" scaled: "), (Gyroscop_zout / 131)) 
        print()
        print("Acceleration sensor")
        print("---------------------")
        acceleration_xout = read_word_2c(0x3b)
        acceleration_yout = read_word_2c(0x3d)
        acceleration_zout = read_word_2c(0x3f)
         
        acceleration_xout_scaled = acceleration_xout / 16384.0
        acceleration_yout_scaled = acceleration_yout / 16384.0
        acceleration_zout_scaled = acceleration_zout / 16384.0
         
        
        print ("acceleration_xout: ", ("%6d" % acceleration_xout), (" scaled: "), acceleration_xout_scaled)
        print ("acceleration_yout: ", ("%6d" % acceleration_yout), (" scaled: "), acceleration_yout_scaled)
        print ("acceleration_zout: ", ("%6d" % acceleration_zout), (" scaled: "), acceleration_zout_scaled)
        print()
        print("Rotation")
        print("---------")
        x_rotation = get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        y_rotation = get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        print("X Rotation: ",x_rotation)     
        print("Y Rotation: ",y_rotation)
        print("---------------------")
        print("")
        time.sleep(10)
        send_to_cloud(x1,y,z1,density,density1,light,fire,temp,humidity,magnetic,acceleration_xout,acceleration_yout,acceleration_zout,Gyroscop_xout,Gyroscop_yout,Gyroscop_zout,x_rotation,y_rotation)
        time.sleep(5)
        
    
    except TypeError:
        print ("type error")
    except IOError:
        print ("IO Error")

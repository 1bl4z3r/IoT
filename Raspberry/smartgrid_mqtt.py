import requests, json
import serial
import time
import paho.mqtt.client as mqtt


#serialCommunication with arduino
ser= serial.Serial('/dev/ttyACM0',9600)
Broker ="59.162.178.178"
port = 1883

client = mqtt.Client()
client.connect(Broker,port)

topic = "device/5b9514005c89ef2b048388e0"

x1=0.0
y1=0.0

print("------------------------------------")
print("------------------------------------")
print(" ")
print("MICRO SMART GRID SYSTEM")
print(" ")
print("------------------------------------")
print("------------------------------------")
print(" ")
print(" ")


    
while True:
    try:
        
        print("------------------------------------")
        print(" ")
        print("Started scanning sensors")
        print(" ")
        print("------------------------------------")

        #serial communication with Arduino
        s = str(ser.readline())
        x=s.split("|")[0]
        y=s.split("|")[1]
        x1=x.split("'")[1]
        y1=y.split("\\")[0]
        #x1=float(x1)*1000
        print("")
        print("RMS Current(mAmps) :",x1)
        print("-----------------------------")
        print("")
        print("Voltage(Volts)     :",y1)
        print("-----------------------------")
        print("")
        data = json.dumps([{"sensor" : "current-sensor", "value":x1, "timestamp":"", "context":"RMS Current Value!!"},
                               {"sensor" : "voltage-sensor", "value":y1, "timestamp":"", "context":"DC Voltage"}])

        client.publish(topic,data)
        
        print("------------------------------------")
        print("------------------------------------")
        print(" ")
        print("Data uploaded")
        print(" ")
        print("------------------------------------")
        print("------------------------------------")
        print(" ")
        print(" ")
        
        time.sleep(5)
        
    
    except TypeError:
        print ("type error")
    except IOError:
        print ("IO Error")

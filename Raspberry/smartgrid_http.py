import requests, json
import serial
import time


#serialCommunication with arduino
ser= serial.Serial('/dev/ttyACM0',9600)

x1=0.0
y1=0.0

url = "http://59.162.178.178:3000/device/micro-smart-grid-system?id=5b9514005c89ef2b048388e0"

def send_to_cloud(x1,y1):
    data = json.dumps([{"sensor" : "current-sensor", "value":y1, "timestamp":"", "context":"RMS Current Value!!"},
                               {"sensor" : "voltage-sensor", "value":x1, "timestamp":"", "context":"DC Voltage"}])

    r=requests.post(url,data)
    print(r.text)   
            
    return
while True:
    try:

        #serial communication with Arduino
        s = str(ser.readline())
        x=s.split("|")[0]
        y=s.split("|")[1]
        x1=x.split("'")[1]
        y1=y.split("\\")[0]
        #x1=float(x1)*1000
        print("")
        print("RMS Current(mAmps)= ",y1)
        print("---------------------")
        print("")
        print("Voltage(Volts) = ",x1)
        print("---------------------")
        print("")
        
        send_to_cloud(x1,y1)
        time.sleep(1)
        
    
    except TypeError:
        print ("type error")
    except IOError:
        print ("IO Error")

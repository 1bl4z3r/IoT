#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

/* Set these to your desired credentials. */
const char *ssid = "xxxxxx";  //ENTER YOUR WIFI SETTINGS
const char *password = "xxxxxx";

//Web/Server address to read/write from 
const char *host = "http://iot.ticollege.org";   //website or IP address of server

int   a,b,c=0;
int   val[1000];
int   value=0;

void setup() {
  Serial.begin(115200);

  pinMode(A0,INPUT);
  pinMode(D5,INPUT);
  pinMode(D6,INPUT);
  WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  //If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP
}

void loop() {
  HTTPClient http;    //Declare object of class HTTPClient
  
  http.begin("http://iot.ticollege.org/reader.php");              //Specify request destination
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header

  while( (digitalRead(D5)==1) || (digitalRead(D6)==1) )
  {
    Serial.println("!");
    digitalRead(D5);
    digitalRead(D6);
  }
  
  for(a=0;a<=999;a++)
  {
    value=analogRead(A0);
    val[a]=value;
    Serial.println(val[a]);     // optional step // just for visualisation
    delay(10);            // 10 millisecond delay is equal to a sampling frequency of 100 Hz
  }
  for(b=0;b<=999;b++)
  {
    Serial.println(val[b]);
    delay(10);
  }
   String data;
  
   for(int c=0;c<=1000;c++)
  {
//    http.POST("data=" + String(d[c]));
    data += String(val[c]) + " ";
    delay(10);
  }
  http.POST("data="+subha1);
//  int httpCode = http.POST(postData);   //Send the request
  String payload = http.getString();    //Get the response payload

//  Serial.println(httpCode);   //Print HTTP return code
  Serial.println(payload);    //Print request response payload

  http.end();  //Close connection
  
  delay(5000);  //Post Data at every 5 seconds
}
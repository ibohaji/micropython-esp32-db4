import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys


def connect_wifi(ssid,password):
    # WiFi connection information
    WIFI_SSID = str(ssid)
    WIFI_PASSWORD = str(password)

    # turn off the WiFi Access Point
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    # connect the device to the WiFi network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)

    # wait until the device is connected to the WiFi network
    MAX_ATTEMPTS = 20
    attempt_count = 0
    while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
        attempt_count += 1
        time.sleep(1)

    if attempt_count == MAX_ATTEMPTS:
        print('could not connect to the WiFi network')
        sys.exit()


def MQTTConnect(username,io_key,feedname):
    # create a random MQTT clientID 
    random_num = int.from_bytes(os.urandom(3), 'little')
    mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

    # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
    # 
    # To use a secure connection (encrypted) with TLS: 
    #   set MQTTClient initializer parameter to "ssl=True"
    #   Caveat: a secure connection uses about 9k bytes of the heap
    #         (about 1/4 of the micropython heap on the ESP8266 platform)
    ADAFRUIT_IO_URL = b'io.adafruit.com' 
    ADAFRUIT_USERNAME = b'ibosen95'
    ADAFRUIT_IO_KEY = b'aio_bTGp22ZlyZkCJwenfGuu2HSMGVJR'
    ADAFRUIT_IO_FEEDNAME = b'Temperature'

    client = MQTTClient(client_id=mqtt_client_id, 
                        server=ADAFRUIT_IO_URL, 
                        user=ADAFRUIT_USERNAME, 
                        password=ADAFRUIT_IO_KEY,
                        ssl=False)
    try:            
        client.connect()
    except Exception as e:
        print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        sys.exit()


# format of feed name:  
#   "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"

def publish(data,feed):
    mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, feed), 'utf-8')
    PUBLISH_PERIOD_IN_SEC = 10 
    while True:
        try:
            client.publish(mqtt_feedname,    
                    bytes(str(data), 'utf-8'), 
                    qos=0)
            time.sleep(PUBLISH_PERIOD_IN_SEC)
        except KeyboardInterrupt:
            print('Ctrl-C pressed...exiting')
            client.disconnect()
            sys.exit()

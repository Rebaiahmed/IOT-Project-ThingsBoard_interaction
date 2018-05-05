# -*- encoding: utf-8 -*-

from xbee import XBee,ZigBee
import serial
import os
import time
import sys
import random as rand
import paho.mqtt.client as mqtt
import json
import io

THINGSBOARD_HOST = '127.0.0.1'
ACCESS_TOKEN = 'Your_Access_Token'
#Serial Port xbee
port="/dev/ttyUSB0"
ser = serial.Serial(port, 9600, timeout=1)  # Le port utilis� /dev/ttyUSB0

xbee= ZigBee(ser)

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

#sensor_data = {'temperature': "0","mouvement":"0"}
sensor_data = {'temperature':"0"}
next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()
#client.publish('v1/devices/me/attributes', json.dumps(sensor_data), 1)
try:
    while True:
        #humidity,temperature = dht.read_retry(dht.DHT22, 4)
      #  mouvement = dict(xbee.wait_read_frame()['samples'][0])['dio-1']#round(humidity, 2)
    # temperature = rand.randint(0,30)#round(temperature, 2)
        transform_tmp = 10.24
        temperature =( dict(xbee.wait_read_frame()['samples'][0] ) ['adc-1'] * 1200 /1024) /10 -32


        print(u"Temperature: {:g}\u00b0C".format(temperature))
        sensor_data['temperature'] = str(temperature)
       # sensor_data['mouvement'] = str(mouvement)


        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/attributes', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

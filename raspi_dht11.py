#!/usr/bin/env python
 
############################################################
# This code uses the Beebotte API, you must have an account.
# You can register here: http://beebotte.com/register
############################################################
 
import time
import Adafruit_DHT
from beebotte import *

_token = '1426111694021_ZCglStK8lAk1PEt7'
_hostname = 'api.beebotte.com'
### Replace ACCESS_KEY and SECRET_KEY with those of your account
bbt = BBT(token = _token, hostname = _hostname)
 
period = 60 ## Sensor data reporting period (1 minute)
pin = 4 ## Assuming the DHT11 sensor is connected to GPIO pin number 4
 
### Change channel name and resource names as suits you
temp_resource   = Resource(bbt, 'RaspberryPi', 'temperature')
humid_resource  = Resource(bbt, 'RaspberryPi', 'humidity')
def convertCtoF(degreesC):
	degreesF =  degreesC * 9/5 + 32
	return degreesF
	
def run():
  while True:
    ### Assume 
    humidity, temperature = Adafruit_DHT.read_retry( Adafruit_DHT.DHT11, pin )
    temperatureF = convertCtoF(temperature)
    if humidity is not None and temperature is not None:
        print "Temp={0:f}*F  Humidity={1:f}%".format(temperatureF, humidity)
        try:
          #Send temperature to Beebotte
          bbt.write("RaspberryPi", "Temperature", temperatureF)
          #Send humidity to Beebotte
          bbt.write("RaspberryPi", "Humidity", humidity)
        except Exception:
          ## Process exception here
          print "Error while writing to Beebotte"
    else:
        print "Failed to get reading. Try again!"
 
    #Sleep some time
    time.sleep( period )
 
run()

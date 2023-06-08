import urllib.request
import RPi.GPIO as GPIO
import time

# set up the ultrasonic sensor pins
TRIG_PIN = 7
ECHO_PIN = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# set up the Thingspeak API parameters
THINGSPEAK_API_KEY = 'THINGSPEAK_WRITE_API_KEY'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# function to measure the distance using the ultrasonic sensor
def get_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == False:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == True:
        end_time = time.time()

    duration = end_time - start_time
    distance = duration * 17150
    distance = round(distance, 2)
    return distance

# main loop
while True:
    distance = get_distance()
    print('Distance: {} cm'.format(distance))

    # upload the distance measurement to Thingspeak
    url = THINGSPEAK_URL + '?api_key=' + THINGSPEAK_API_KEY + '&field1=' + str(distance)
    urllib.request.urlopen(url)

    time.sleep(5)

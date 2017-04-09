import RPi.GPIO as GPIO
import time

sensor = 4
led = 17
redled = 21


GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(redled, GPIO.OUT, initial=GPIO.LOW)
previous_state = False
current_state = False

def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(1)  
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(1)  
        return  

while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s" % (sensor, new_state))
        if new_state=="HIGH":
            GPIO.output(redled,GPIO.HIGH)
            time.sleep(1)
            blink(led)
GPIO.cleanup()

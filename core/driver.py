from machine import Pin, PWM
import time

ain1 = Pin(18, Pin.OUT)
ain2 = Pin(19, Pin.OUT)
stby = Pin(4, Pin.OUT)

pwma = PWM(Pin(5), freq=1000)

def motor_forward(speed):
    stby.value(1)
    stby.value(1)
    stby.value(0)
    pwma.duty(speed)

def motor_stop():
    pwma.duty(0)
    stby.value(0)

# Test

motor_forward(512)
time.sleep(4)
motor_stop
    
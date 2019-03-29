import  gpiozero
from gpiozero import Servo
from time import sleep
import pigpio

from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
#gpiozero.Device.pin_factory = PiGPIOFactory()

pi = pigpio.pi()

while True:
    pi.set_servo_pulsewidth(5, 700)
    pi.set_servo_pulsewidth(12, 700)
    pi.set_servo_pulsewidth(24, 700)
    sleep(1)
    pi.set_servo_pulsewidth(5, 1250)
    pi.set_servo_pulsewidth(12, 1250)
    pi.set_servo_pulsewidth(24, 1250)
    sleep(1)
    pi.set_servo_pulsewidth(5, 2000)
    pi.set_servo_pulsewidth(12, 2000)
    pi.set_servo_pulsewidth(24, 2000)
    sleep(1)


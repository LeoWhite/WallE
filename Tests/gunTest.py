from gpiozero import Servo
from time import sleep

servo = Servo(13, initial_value=-0.2)
#servo.min()
sleep(1)
servo.value=-0.3
sleep(0.1)


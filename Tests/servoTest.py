from gpiozero import Servo
from time import sleep

servo = Servo(5)
servo2 = Servo(12)
servo3 = Servo(24)
while True:
    servo.min()
    servo2.min()
    servo3.min()
    sleep(1)
    servo.mid()
    servo2.mid()
    servo3.mid()
    sleep(1)
    servo.max()
    servo2.max()
    servo3.max()
    sleep(1)


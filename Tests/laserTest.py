from gpiozero import DigitalOutputDevice
from time import sleep

laser = DigitalOutputDevice(17, active_high=False)

sleep(5)

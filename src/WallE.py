from robot import Robot
from gpiozero import Servo, LED, Button
import atexit
import time

#from gpiozero.pins.pigpiod import PiGPIOPin
#import gpiozero.devices
#gpiozero.devices.pin_factory = PiGPIOPin

# The WallE class builds on top of the base robot, setting up items that
# are specific to WallE (e.g. arms, head)


#pg.mixer.init()
#pg.init()

#a1Note = pg.mixer.Sound("F:\Project Harpsichord\The wavs\A1.wav")
#a2Note = pg.mixer.Sound("F:\Project Harpsichord\The wavs\A0.wav")

#pg.mixer.set_num_channels(50)

#for i in range(25):
#    a1Note.play()
#    time.sleep(0.3)
#    a2Note.play()
#    time.sleep(0.3)
    
    
    
class WallE(Robot):
  # Configure the battery ranges. Wall-E is powered by a 3S battery
  battery_min = 9.6
  battery_max = 12.6
  
  def __init__(self, playButtonCallback=None):
    Robot.__init__(self)
    
    print('Setting up WallE')
    
    # Ensure the battery range is correctly set
    self._tb.SetBatteryMonitoringLimits(self.battery_min, self.battery_max)

    battMin, battMax = self._tb.GetBatteryMonitoringLimits()
    battCurrent = self._tb.GetBatteryReading()
    print 'Current battery monitoring settings:'
    print '    Minimum  (red)     %02.2f V' % (battMin)
    print '    Half-way (yellow)  %02.2f V' % ((battMin + battMax) / 2)
    print '    Maximum  (green)   %02.2f V' % (battMax)
    print
    print '    Current voltage    %02.2f V' % (battCurrent)
    print
    self._tb.SetLedShowBattery(True)

    # Setup/center HEAD
    self._head = Servo(24)
    
    # Setup the left arm
    self._leftArm = Servo(5)
    
    # Setup the right arm
    self._rightArm = Servo(12)
    
    # Setup the gun servo
    #self._gun = Servo(13, initial_value=-0.15)
    
    # Center the servos
    self.center_servos()
    
    
    
    # Setup the eyes
    self._eyes = LED(25)
    # self._eyes.on()
    
    # Setup the play button
    self._playButton = Button(23)

    if playButtonCallback != None:
      self._playButton.when_pressed = playButtonCallback
    
    # Ensure the motors get stopped when the code exits
    atexit.register(self.center_servos)

  def set_left_arm(self, position):
    self._leftArm.value = position
  
  def set_right_arm(self, position):
    self._rightArm.value = position
  
  def set_head_pan(self, position):
    self._head.value = position
    
  def fire_gun():
    self._gun.value = -0.3
    time.sleep(0.1)
    self._gun.value = -0.2
  
  def center_servos(self):
    self.set_left_arm(0)
    self.set_right_arm(0)
    self.set_head_pan(0)

  
    


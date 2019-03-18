from robot import Robot
from gpiozero import Servo, LED
import atexit
import time

# The WallE class builds on top of the base robot, setting up items that
# are specific to WallE (e.g. arms, head)


class WallE(Robot):
  # Configure the battery ranges. Wall-E is powered by a 3S battery
  battery_min = 9.6
  battery_max = 12.6
  
  def __init__(self):
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
    
    # Center the servos
    self.center_servos()
    
    # Setup the eyes
    self._eyes = LED(25)
    # self._eyes.on()
    
    # Ensure the motors get stopped when the code exits
    atexit.register(self.center_servos)

  def set_left_arm(self, position):
    self._leftArm.value = position
  
  def set_right_arm(self, position):
    self._rightArm.value = position
  
  def set_head_pan(self, position):
    self._head.value = position
  
  def center_servos(self):
    self.set_left_arm(0)
    self.set_right_arm(0)
    self.set_head_pan(0)

  
    


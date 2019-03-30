from robot import Robot
from gpiozero import Servo, LED, Button
import atexit
import time
import pigpio
    
    
class WallE(Robot):
  # Configure the battery ranges. Wall-E is powered by a 3S battery
  battery_min = 9.6
  battery_max = 12.6
  
  servo_mid_point = 1500
  servo_range = 180
  
  def __init__(self, playButtonCallback=None):
    Robot.__init__(self)
    
    print('Setting up WallE')
    
    # Init PIGPIO
    self._pigpio =  pigpio.pi()
    
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

    # Setup/center HEAD (650,800,950)
    self._head = 24
    
    # Setup the left arm
    self._leftArm = 5
    
    # Setup the right arm
    self._rightArm = 12
    
    # Setup the gun servo
    self._gun = 13
    
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
    atexit.register(self.exit)

  def set_left_arm(self, position):
    value = self.servo_mid_point + (position * self.servo_range)
    self._pigpio.set_servo_pulsewidth(self._leftArm, value)
  
  def set_right_arm(self, position):
    value = self.servo_mid_point + (position * self.servo_range)
    self._pigpio.set_servo_pulsewidth(self._rightArm, value)
  
  def set_head_pan(self, position):
    value = self.servo_mid_point + (position * self.servo_range)
    self._pigpio.set_servo_pulsewidth(self._head, value)
    
  def fire_gun():
    self._gun.value = -0.3
    time.sleep(0.1)
    self._gun.value = -0.2
  
  def center_servos(self):
    self.set_left_arm(0)
    self.set_right_arm(0)
    self.set_head_pan(0)
  
  def exit(self):
    self.center_servos()
    self._pigpio.stop()
    

  
    


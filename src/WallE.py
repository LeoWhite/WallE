from robot import Robot
from gpiozero import Servo
import atexit
import time

# The WallE class builds on top of the base robot, setting up items that
# are specific to WallE (e.g. arms, head)


class WallE(Robot):
  def __init__(self):
    Robot.__init__(self)
    
    print('Setting up WallE')
    
    # Setup/center HEAD
    self._head = Servo(5)
    
    # Setup the left arm
    self._leftArm = Servo(24)
    
    # Setup the right arm
    self._rightArm = Servo(12)
    
    # Center the servos
    self.center_servos()
    
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

  
    


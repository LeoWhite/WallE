from WallE import WallE
from time import sleep
from robot import EncoderCounter
import numpy as np

class FollowLineBehavior(object):
    """Follows a line"""
    def __init__(self, WallE):
        self._WallE = WallE

        sensitivity = 100
        self.low_range = np.array([0,0,255-sensitivity])
        self.high_range = np.array([255,sensitivity,255])

    def driveCallback(self, drive_straight):
      # Just keep driving
      return True

    def run(self):      
        self._WallE.drive_to_colour(self.driveCallback, self.low_range, self.high_range, 0.45)

if __name__ == '__main__':
  buttonPressed = False
  
  # Allow some time for the camera to settle
  def playButtonCallback():
    global buttonPressed
    buttonPressed = True

  behavior = FollowLineBehavior(WallE(playButtonCallback))
  

  while True:
    if buttonPressed:
      buttonPressed = False
      # Allow time for the user to back away
      sleep(1)
      
      # Start following
      behavior.run()


    sleep(0.1)

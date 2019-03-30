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
        self._WallE.drive_to_colour(self.driveCallback, self.low_range, self.high_range, 0.5)

if __name__ == '__main__':   
  behavior = FollowLineBehavior(WallE())
  
  # Allow some time for the camera to settle
  sleep(5)
  behavior.run()

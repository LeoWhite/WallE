from WallE import WallE
from time import sleep
from robot import EncoderCounter

class ObstacleAvoidingBehavior(object):
    """Better obstacle avoiding"""
    def __init__(self, WallE):
        self._WallE = WallE

        self.max_distance = 150

    def driveCallback(self, drive_straight):
      # Read in the current distance
      distance = self._WallE.get_distance()

      #print("Distances: l", distance)
      
      # Still got further to go?
      if distance > self.max_distance:        
        # Allow time for travel      
        #sleep(0.005)
        
        return True
        
      return False

    def run(self):      
        # Start driving forwards
        self._WallE.drive_straight(self.driveCallback, 0.6)

behavior = ObstacleAvoidingBehavior(WallE())
behavior.run()

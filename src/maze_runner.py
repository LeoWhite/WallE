from WallE import WallE
from robot import EncoderCounter
from pid_controller import PIController
import time

class MazeRunnerBehaviour(object):
    """Simple maze running cod"""
    def __init__(self, WallE):
        self._WallE = WallE

        self._max_distance_from_wall = 250
        
        # Use left as "primary"  motor, the right is keeping up
        self.set_primary        = self._WallE.set_left
        self.primary_encoder    = self._WallE.left_encoder
        self.set_secondary      = self._WallE.set_right
        self.secondary_encoder  = self._WallE.right_encoder


    def drive_to_wall(self, speed):
          # Create a new PI controller for going straight
          controller = PIController(proportional_constant=0.015, integral_constant=0.002)

          # Reset the encoders
          self.primary_encoder.reset()
          self.secondary_encoder.reset()
          
          # Start moving forwards
          self._WallE.set_motors(speed)

          # First we want to drive to the next wall
          distance = self._WallE.get_distance()
          while distance > self._max_distance_from_wall:
            print("Distance ", distance)
            # Allow the robot to drive
            time.sleep(0.02)
            
            # How far off are we?
            error = self.primary_encoder.pulse_count - self.secondary_encoder.pulse_count
            adjustment = controller.get_value(error)
            adjustment = adjustment / 100
            # How fast should the motor move to get there?
            self.set_secondary(speed + adjustment)
            
            # Update the distance (For testing purposes, so we can output it)
            distance = self._WallE.get_distance()

    def turn_90_degrees(self, speed, direction):          
          if direction == 'L':
            print("Turning left!")
            # Robot needs to be moving 'backwards'
            speed = -(abs(speed))
          else:
            print("Turning right!")
            # Robot needs to be moving 'forwards'
            speed = abs(speed)
          
          self._WallE.drive_arc(90, 0, speed=speed)

          print("Done!")
 

    def run(self, mazeMap, speed=0.75):    
        # Iterate over each direction in the maze map
        for turn in mazeMap:
          # First we want to drive to the next wall
          self.drive_to_wall(speed)
          
          # Stop!
          self.set_primary(0)
          self.set_secondary(0)
          
          # What direction do we want to turn?
          self.turn_90_degrees(speed, turn)

          self.set_primary(0)
          self.set_secondary(0)

behaviour = MazeRunnerBehaviour(WallE())
behaviour.run("L", 0.75)


from WallE import WallE
from robot import EncoderCounter
from pid_controller import PIController
import time
import math

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

          self.primary_encoder.set_direction(math.copysign(1, speed))
          self.secondary_encoder.set_direction(math.copysign(1, speed))

          # Reset the encoders
          self.primary_encoder.reset()
          self.secondary_encoder.reset()
          
          # Start moving forwards
          self._WallE.set_motors(speed)

          # First we want to drive to the next wall
          distance = self._WallE.get_distance()
          print("Distance ", distance)
          while distance > self._max_distance_from_wall:
            # Allow the robot to drive
            time.sleep(0.01)
            
            # How far off are we?
            error = self.primary_encoder.pulse_count - self.secondary_encoder.pulse_count
            print("Error ",error)
            adjustment = controller.get_value(error)
            # How fast should the motor move to get there?
            self.set_secondary(speed + adjustment)
            self.secondary_encoder.set_direction(math.copysign(1, speed+adjustment))
            
            # Update the distance (For testing purposes, so we can output it)
            distance = self._WallE.get_distance()
            print("Distance ", distance)

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
          print("Driving to wall")
          self.drive_to_wall(speed)
          
          # Stop!
          self._WallE.set_motors(0)
          time.sleep(1)
          
          # What direction do we want to turn?
          print("Turning to ",turn)
          self.turn_90_degrees(speed, turn)

          self._WallE.set_motors(0)
          time.sleep(1)

behaviour = MazeRunnerBehaviour(WallE())
behaviour.run("LLRRLLLR", 0.6)


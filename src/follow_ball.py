from WallE import WallE
import os
import atexit
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
import time
from collections import namedtuple
import pi_camera_stream
import numpy as np

# Key mappings. Move to a seperate class?
PS3_SELECT = 8
PS3_L3 = 11
PS3_R3 = 12
PS3_START = 9
PS3_DPAD_UP = 13
PS3_DPAD_RIGHT = 16
PS3_DPAD_DOWN = 14
PS3_DPAD_LEFT = 15
PS3_L2 = 6
PS3_R2 = 7
PS3_L1 = 4
PS3_R1 = 5
PS3_TRIANGLE = 2
PS3_CIRCLE = 1
PS3_CROSS =  0
PS3_SQUARE = 3
PS3_PLAYSTATION = 10

PS3_AXIS_LEFT_H = 0
PS3_AXIS_LEFT_V = 1
PS3_AXIS_RIGHT_H = 2
PS3_AXIS_RIGHT_V = 3
PS3_AXIS_DPAD_UP = 8
PS3_AXIS_DPAD_RIGHT = 9
PS3_AXIS_DPAD_DOWN = 10
PS3_AXIS_DPAD_LEFT = 11 
PS3_AXIS_L2 = 12
PS3_AXIS_R2 = 3
PS3_AXIS_L1 = 14
PS3_AXIS_R1 = 15
PS3_AXIS_TRIANGLE = 16
PS3_AXIS_CIRCLE = 17
PS3_AXIS_CROSS =  18
PS3_AXIS_SQUARE = 19
PS3_AXIS_PLAYSTATION = 16


sensitivity = 20
lowerBound=np.array([140-sensitivity,60,50])
upperBound=np.array([140+sensitivity,255,255])

running = False
 
# Allows direct manual control of WallE via a PS3 controller
class FollowBall(object):
  def __init__(self, WallE):
    self._WallE = WallE
    self._driveLeft = 0.0
    self._driveRight = 0.0
    
    self._headPan = 0.0
    self._encoderTravel = 0
    
    # Play the startup sound
    soundStartup.play()
    
    # Make sure we release it at exit
    atexit.register(self.shutdown)

  def driveCallback(self, drive_straight):
    global running

    # Keep driving unless told to stop
    return running
        
  def run(self, speed, turn_speed):
    global running
    # Turn until colour is detected
    
    # Drive toward ball until hit it.
    running = True

    while running:
      # Turn in a circl
      self._WallE.set_left(turn_speed)
      self._WallE.set_right(-turn_speed)

      # Check for the colour
      for frame in pi_camera_stream.start_stream(self._WallE._camera):
        # Check for colour
        (x, y), radius = self._WallE.process_frame(frame, lowerBound, upperBound)
        
        if radius > 20 or running == False:
          break

      # Stop
      self._WallE.stop_motors()
      
      # Drive to 
      self._encoderTravel = 0
      self._WallE.drive_to_colour(self.driveCallback, lowerBound, upperBound, speed)
    
      time.sleep(1)
      
      self._WallE.stop_motors()
      
      

    self._WallE.stop_motors()
        
  def shutdown(self):
    self._WallE.set_left(0)
    self._WallE.set_right(0)

if __name__ == '__main__':
  # Setup pygame
  # Initialise the pygame library, ready for use
  pygame.init()
 
  # Setup the music
  audioVolume = 1
  pygame.mixer.init()
  pygame.mixer.music.set_volume(audioVolume)

  # and preload the samples
  musicAudioChannel = None
  musicAudio = pygame.mixer.Sound("/home/pi/Audio/PutOnYourSundayClothes.wav")
  musicAudio.set_volume(audioVolume)

  soundStartup = pygame.mixer.Sound("/home/pi/Audio/Startup.wav")
  soundStartup.set_volume(audioVolume)

  def playButtonCallback():
    global running
    
    print "Stopping"
    running = False

  behaviour=FollowBall(WallE(playButtonCallback))
  behaviour.run(0.75, 0.65)

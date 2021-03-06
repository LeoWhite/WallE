from WallE import WallE
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
import atexit
import os
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

ColourStruct = namedtuple("ColourStruct", "colour low high")


colours=[]
colours.append(ColourStruct("red", np.array([160,100,50]), np.array([179,255,255])))
colours.append(ColourStruct("blue", np.array([100,100,50]), np.array([120,255,255])))
colours.append(ColourStruct("yellow", np.array([5,100,50]), np.array([30,255,255])))
colours.append(ColourStruct("green", np.array([60-20,100,50]), np.array([60+20,255,255])))
 
# Allows direct manual control of WallE via a PS3 controller
class Nebula(object):
  def __init__(self, WallE):
    self._WallE = WallE
    self._driveLeft = 0.0
    self._driveRight = 0.0
    
    self._headPan = 0.0
    self._max_distance_from_wall = 150
    self._encoderTravel = 0

    # Connect up to the joystick
    while pygame.joystick.get_count() == 0:
      self._WallE.set_led(0,0,1)
      pygame.joystick.quit()
      time.sleep(1)
      self._WallE.set_led(0,0,0)
      pygame.joystick.init()
    
    # Got a joystick, change LED to green and set it up
    self._WallE.set_led(0,1,0)
    self._j = pygame.joystick.Joystick(0)
    self._j.init()    

    # Play the startup sound
    soundStartup.play()
    
    # Make sure we release it at exit
    atexit.register(self.shutdown)

  def driveCallback(self, drive_straight):
    self._encoderTravel = drive_straight
    
    # Read in the current distance
    distance = self._WallE.get_distance()

    #print("Distances: l", distance)
    
    # Still got further to go?
    if distance > self._max_distance_from_wall:        
      # Allow time for travel      
      #sleep(0.005)
      
      return True
      
    return False
        
  def runNebula(self, speed):
    # Plan of attack
    
    
    for colour in colours:      
      # Check for the colour
      for frame in pi_camera_stream.start_stream(self._WallE._camera):
        # Check for colour
        (x, y), radius = self._WallE.process_frame(frame, colour.low, colour.high)
        
        if radius > 20:
          break
      
        # Turn 45 to next detection point
        self._WallE.drive_arc(45, 0, speed=speed)
      
      # Drive to 
      self._encoderTravel = 0
      self._WallE.drive_to_colour(self.driveCallback, colour.low, colour.high, speed)
    
      time.sleep(0.1)
      
      # Reverse
      print("encoder: l", self._encoderTravel)
      if self._encoderTravel > 0:
        self._WallE.drive_distances(self._encoderTravel, self._encoderTravel, -speed)
      
    self._WallE.stop_motors()
    
    
  def run(self):
    global soundWallE

    # Run for ever
    running = True
   
    pygame.event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]) 

    while running:
      # Read in the queued up events
      events = pygame.event.get()
      
      for event in events:
        updateValues = False
      
        if event.type == pygame.QUIT:
          # User exit
          running = False

        elif event.type == pygame.JOYBUTTONDOWN:
            # A button on the joystick just got pushed down
            updateValues = True
            if event.button == PS3_DPAD_DOWN:
              soundWallE.play()
            elif event.button == PS3_DPAD_LEFT:
                self._WallE.set_head_pan(-1)
            elif event.button == PS3_DPAD_RIGHT:
                self._WallE.set_head_pan(1)
            elif event.button == PS3_DPAD_UP:
                self._WallE.set_right_arm(1)
            elif event.button == PS3_CROSS: 
             self.runNebula(0.75)
        elif event.type == pygame.JOYBUTTONUP:
            # A button on the joystick just got pushed down
            updateValues = True
            if event.button == PS3_DPAD_DOWN:
              soundWallE.play()
            elif event.button == PS3_DPAD_LEFT:
                self._WallE.set_head_pan(0)
            elif event.button == PS3_DPAD_RIGHT:
                self._WallE.set_head_pan(0)
            elif event.button == PS3_DPAD_UP:
                self._WallE.set_right_arm(0)
    
    
  def shutdown(self):
    self._WallE.set_left(0)
    self._WallE.set_right(0)
    self._j.quit()

if __name__ == '__main__':    
  # Setup pygame
  # Initialise the pygame library, ready for use
  #os.environ["SDL_VIDEODRIVER"] = "dummy"
  pygame.init()
  pygame.display.set_mode((1,1))
 
  # Setup the music
  audioVolume = 1
  pygame.mixer.init()
  pygame.mixer.music.set_volume(audioVolume)

  # and preload the samples
  musicAudioChannel = None
  musicAudio = pygame.mixer.Sound("/home/pi/Audio/PutOnYourSundayClothes.wav")
  musicAudio.set_volume(audioVolume)

  soundGun = pygame.mixer.Sound("/home/pi/Audio/Gun.wav")
  soundGun.set_volume(audioVolume)
  soundStartup = pygame.mixer.Sound("/home/pi/Audio/Startup.wav")
  soundStartup.set_volume(audioVolume)
  soundWallE = pygame.mixer.Sound("/home/pi/Audio/Walle2.wav")
  soundWallE.set_volume(audioVolume)

  def playButtonCallback():
    global musicAudioChannel
    
    if musicAudioChannel == None or False == musicAudioChannel.get_busy():
      musicAudioChannel = musicAudio.play()
    else:
      musicAudioChannel.stop()

  behaviour=Nebula(WallE(playButtonCallback))
  behaviour.run()

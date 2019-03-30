from WallE import WallE
import pygame
import atexit
import os
import time

# Key mappings. Move to a seperate class?
PS3_SELECT = 0
PS3_L3 = 1
PS3_R3 = 2
PS3_START = 3
PS3_DPAD_UP = 4
PS3_DPAD_RIGHT = 5
PS3_DPAD_DOWN = 6
PS3_DPAD_LEFT = 7
PS3_L2 = 8
PS3_R2 = 9
PS3_L1 = 10
PS3_R1 = 11
PS3_TRIANGLE = 12
PS3_CIRCLE = 13
PS3_CROSS =  14
PS3_SQUARE = 15
PS3_PLAYSTATION = 16

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

# Allows direct manual control of WallE via a PS3 controller
class ManualDriveBehaviour(object):
  def __init__(self, WallE):
    self._WallE = WallE
    self._driveLeft = 0.0
    self._driveRight = 0.0

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
    
  def run(self):
    # TODO: Set arms and heads to default locations
    driveUpDown = 0.0
    driveLeftRight = 0.0
    
    # Run for ever
    running = True
    
    while running:
      # Read in the queued up events
      events = pygame.event.get()
      
      for event in events:
        updateValues = False
      
        if event.type == pygame.QUIT:
          # User exit
          running = False

        # Have the joysticks moved?
        elif event.type == pygame.JOYAXISMOTION:
          updateValues = True
        elif event.type == pygame.JOYBUTTONDOWN:
            # A button on the joystick just got pushed down
            updateValues = True
            if event.button == PS3_DPAD_DOWN:
              global soundWallE
              soundWallE.play()
            #elif event.button == PS3_CROSS: 
             # self._WallE.fire_gun()
            
        
        # Anything to process?
        if updateValues:
          # Read in the current values
          driveUpDown = self._j.get_axis(PS3_AXIS_LEFT_V)
          driveLeftRight = self._j.get_axis(3)
          
          # print("V ", driveUpDown, "H ", driveLeftRight)
          
          # Determine the drive power levels
          self._driveLeft = -driveUpDown
          self._driveRight = -driveUpDown
          if driveLeftRight < -0.05:
              # Turning left
              self._driveLeft *= 1.0 + (2.0 * driveLeftRight)
          elif driveLeftRight > 0.05:
              # Turning right
              self._driveRight *= 1.0 - (2.0 * driveLeftRight)
          
          # Update the motors
          self._WallE.set_left(self._driveLeft)
          self._WallE.set_right(self._driveRight)
          
          # Check for any other button presses
          
    
    
  def shutdown(self):
    self._WallE.set_left(0)
    self._WallE.set_right(0)
    self._j.quit()

if __name__ == '__main__':    
  # Setup pygame
  # Initialise the pygame library, ready for use
  os.environ["SDL_VIDEODRIVER"] = "dummy"
  pygame.init()
    
  # Setup the music
  audioVolume = 0.2
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

  behaviour=ManualDriveBehaviour(WallE(playButtonCallback))
  behaviour.run()

from gpiozero import Button
import pygame
import time
import os

os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
pygame.init()
#pygame.display.set_mode((1,1))


pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

musicAudioChannel = None
musicAudio = pygame.mixer.Sound("/home/pi/Audio/PutOnYourSundayClothes.wav")
musicAudio.set_volume(0.2)

def playButtonCallback():
  global musicAudioChannel
  
  if musicAudioChannel == None or False == musicAudioChannel.get_busy():
    musicAudioChannel = musicAudio.play()
  else:
    musicAudioChannel.stop()


button = Button(23)
button.when_pressed = playButtonCallback

while True:
  time.sleep(1)
  


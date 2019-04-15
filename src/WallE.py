from robot import Robot
from gpiozero import Servo, LED, Button
from pid_controller import PIController
import math
import atexit
import time
import pigpio
from gpiozero import DigitalOutputDevice


# Include camera and openCV for image processing
import cv2
import numpy as np
import pi_camera_stream
    
    
class WallE(Robot):
  # Configure the battery ranges. Wall-E is powered by a 3S battery
  battery_min = 9.6
  battery_max = 12.6
  
  servo_mid_point = 1500
  servo_range = 180

  correct_radius = 120
  center = 160
  
  _debug = True

  def __init__(self, playButtonCallback=None):
    Robot.__init__(self)
    
    print('Setting up WallE')
    
    # Init PIGPIO
    self._pigpio =  pigpio.pi()
    
    # Ensure the battery range is correctly set
    self._tb.SetBatteryMonitoringLimits(self.battery_min, self.battery_max)

    battMin, battMax = self._tb.GetBatteryMonitoringLimits()
    battCurrent = self._tb.GetBatteryReading()
    print 'Current battery monitoring settings:'
    print '    Minimum  (red)     %02.2f V' % (battMin)
    print '    Half-way (yellow)  %02.2f V' % ((battMin + battMax) / 2)
    print '    Maximum  (green)   %02.2f V' % (battMax)
    print
    print '    Current voltage    %02.2f V' % (battCurrent)
    print
    self._tb.SetLedShowBattery(True)

    # Setup/center HEAD (650,800,950)
    self._head = 24
    
    # Setup the left arm
    self._leftArm = 5
    
    # Setup the right arm
    self._rightArm = 12
    
    # Setup the gun servo
    #self._gun = 13
    #self._laser = DigitalOutputDevice(17, active_high=False)
    
    # Center the servos
    self.center_servos()
    
    # Setup the eyes
    self._eyes = LED(25)
    # self._eyes.on()
    
    # Setup the play button
    self._playButton = Button(23)

    if playButtonCallback != None:
      self._playButton.when_pressed = playButtonCallback
    
    # Startup camera
    self._camera = pi_camera_stream.setup_camera()

    # Ensure the motors get stopped when the code exits
    atexit.register(self.exit)

  def set_left_arm(self, position):
    value = self.servo_mid_point + (position * 250)
    self._pigpio.set_servo_pulsewidth(self._leftArm, value)
  
  def set_right_arm(self, position):
    value = self.servo_mid_point + (position * 250)
    self._pigpio.set_servo_pulsewidth(self._rightArm, value)
  
  def set_head_pan(self, position):
    value = self.servo_mid_point + (position * self.servo_range)
    self._pigpio.set_servo_pulsewidth(self._head, value)
    
  def fire_gun(self):
    #self._pigpio.set_servo_pulsewidth(self._gun, 1425)
    time.sleep(0.5)
    #self._pigpio.set_servo_pulsewidth(self._gun, 1500)
  
  def center_servos(self):
    self.set_left_arm(0)
    self.set_right_arm(0)
    self.set_head_pan(0)
    #self._pigpio.set_servo_pulsewidth(self._gun, 1500)
  
  def exit(self):
    self.center_servos()
    self._pigpio.stop()

  def find_object(self, original_frame, low_range, high_range):
      """Find the largest enclosing circle for all contours in a masked image.
      Returns: the masked image, the object coordinates, the object radius"""
      frame_hsv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2HSV)
      masked = cv2.inRange(frame_hsv, low_range, high_range)

      # Find the contours of the image (outline points)
      contour_image = np.copy(masked)
      contours, _ = cv2.findContours(contour_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      # Find enclosing circles
      circles = [cv2.minEnclosingCircle(cnt) for cnt in contours]
      # Filter for the largest one
      largest = (0, 0), 0
      for (x, y), radius in circles:
          if radius > largest[1]:
              largest = (int(x), int(y)), int(radius)
      return masked, largest[0], largest[1]


  def process_frame(self, frame_orig, low_range, high_range):
      # Crop the frame
      frame = frame_orig
      
      
      #frame = frame_orig
      # Find the largest enclosing circle
      masked, coordinates, radius = self.find_object(frame, low_range, high_range)
      
      if self._debug:
        # Now back to 3 channels for display
        processed = cv2.cvtColor(masked, cv2.COLOR_GRAY2BGR)
        # Draw our circle on the original frame, then display this
        cv2.circle(frame, coordinates, radius, [255, 0, 0])
        cv2.imshow('output',frame)
        cv2.waitKey(1)
      
      # Yield the object details
      return coordinates, radius


  def drive_to_colour(self, callback, low_range, high_range, speed=0.75):
      self.left_encoder.reset()
      self.right_encoder.reset()

      # Direction controller
      controller = PIController(proportional_constant=0.0015, integral_constant=0.0000, windup_limit=400)

      # Ensure that the encoder knows which way it is going
      self.left_encoder.set_direction(math.copysign(1, speed))
      self.right_encoder.set_direction(math.copysign(1, speed))

      # start the loop
      for frame in pi_camera_stream.start_stream(self._camera):
        # Time to exit?
        if callback(self.left_encoder.pulse_count) == False:
          break
          
        # Process the frame
        (x, y), radius = self.process_frame(frame, low_range, high_range)
        
        if radius > 20:
            # The size is the first error
            radius_error = self.correct_radius - radius
            #speed_value = speed_pid.get_value(radius_error)
            # And the second error is the based on the center coordinate.
            direction_error = self.center - x
            direction_value = controller.get_value(direction_error)
            
            if self._debug:
              print("radius: %d, radius_error: %d direction_error: %d, direction_value: %.2f" %
                  (radius, radius_error, direction_error, direction_value))
            
            # Now produce left and right motor speeds
            self.set_left(speed - direction_value)
            self.set_right(speed + direction_value)
        else:
            self.stop_motors()
            break
  

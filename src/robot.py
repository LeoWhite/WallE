import ThunderBorg
import atexit
import sys

from encoder_counter import EncoderCounter

# Main code base for a ThunderBorg based robot.

class Robot(object):
    wheel_diameter_mm = 60.0
    ticks_per_revolution = 63.0 * 20 # Gear ratio * 20
    wheel_distance_mm =  175.0

    def __init__(self, thunderBorgI2CAddress=0x15, drive_enabled=True):
        # Create an instance of the TB board and initialise it
        self._tb = ThunderBorg.ThunderBorg()
        self._tb.i2cAddress = thunderBorgI2CAddress
        self._tb.Init()

        # Did we find it?
        if not self._tb.foundChip:
          print('No ThunderBorg found, please check connections')
          sys.exit()
          
        # Setup communications failsafe
        failsafe = False
        for i in range(5):
          self._tb.SetCommsFailsafe(True)
          failsafe = self._tb.GetCommsFailsafe()
          if failsafe:
            break
        if not failsafe:
          print('Board %02X failed to report in failsafe mode!' % (self._tb.i2cAddress))
          sys.exit()

        # Abstract out the motor numbers
        self.left_motor = self._tb.SetMotor1
        self.right_motor = self._tb.SetMotor2
        self.drive_enabled = drive_enabled
        self._tb.MotorsOff()

        # Setup the battery indicator LED
        self._tb.SetLedShowBattery(False)
        
        # Ensure the motors get stopped when the code exits
        atexit.register(self.stop_all)
        
        # TODO: Set up the distance sensor
        
        # TODO: Setup the encoders
        #EncoderCounter.set_constants(self.wheel_diameter_mm, self.ticks_per_revolution)
        #self.left_encoder = EncoderCounter(4)
        #self.right_encoder = EncoderCounter(26)
        
        # TODO: Setup any extra LEDS
        
        # TODO: Setup servos for pan-tilt if needed
        
    def stop_all(self):
      # Stop the motors
      self.stop_motors();
      
      # Clear any sensors
      
      # Clear the display
      
      # Reset servos
      
    
    def set_left(self, speed):
      if not self.drive_enabled:
        return;
        
      # TODO: Validate speed, adjust for MAX power limitations
      self.left_motor(speed)

    def set_right(self, speed):
      if not self.drive_enabled:
        return;
        
      # TODO: Validate speed, adjust for MAX power limitations
      self.right_motor(speed)
    
    def stop_motors(self):
      self._tb.MotorsOff()

    def set_pan(self, angle):
      # TODO: Set the PAN location
      return

    def set_tilt(self, angle):
      # TODO: Set the Tilt servo
      return
    
    def set_led(self, r, g, b):
      self._tb.SetLeds(r, g, b)


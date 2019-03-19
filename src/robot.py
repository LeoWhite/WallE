import ThunderBorg
import atexit
import sys

from encoder_counter import EncoderCounter
from distance_sensor_vl53l1x import DistanceSensor
from pid_controller import PIController
import math
from time import sleep

# Main code base for a ThunderBorg based robot.

class Robot(object):
    wheel_diameter_mm = 56.0
    ticks_per_revolution = 63.0 * 10 # Gear ratio * 10 (We are only counting one channel of the encoder, otherwise it would be * 20)
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
          
        # Force communication failsafe to off, as some of the scripts do not update
        # calls too often
        failsafe = False
        for i in range(5):
          self._tb.SetCommsFailsafe(False)
          failsafe = self._tb.GetCommsFailsafe()
          if not failsafe:
            break
        if failsafe:
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
        self.distance_sensor = DistanceSensor()
        
        # Setup the encoders
        EncoderCounter.set_constants(self.wheel_diameter_mm, self.ticks_per_revolution)
        self.left_encoder = EncoderCounter(26)
        self.right_encoder = EncoderCounter(6)
        
        # TODO: Setup any extra LEDS
        
        # TODO: Setup servos for pan-tilt if needed
        
    def stop_all(self):
      # Stop the motors
      self.stop_motors();
      
      # Clear any sensors
      
      # Clear the display
      
      # Reset servos
      
    
    def set_motors(self, speed):
      """Sets both motors to the same speed"""
      if not self.drive_enabled:
        return;
        
      # TODO: Validate speed, adjust for MAX power limitations
      
      self._tb.SetMotors(speed)

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

    def get_distance(self):
      return self.distance_sensor.get_distance()

    def drive_distances(self, left_distance, right_distance, speed=0.75):
        # We always want the "primary" to be the longest distance, therefore the faster motor
        if abs(left_distance) >= abs(right_distance):
            print("Left is primary")
            set_primary        = self.set_left
            primary_encoder    = self.left_encoder
            set_secondary      = self.set_right
            secondary_encoder  = self.right_encoder
            primary_distance   = left_distance
            secondary_distance = right_distance
        else:
            print("right is primary")
            set_primary        = self.set_right
            primary_encoder    = self.right_encoder
            set_secondary      = self.set_left
            secondary_encoder  = self.left_encoder
            primary_distance   = right_distance
            secondary_distance = left_distance
        primary_to_secondary_ratio = secondary_distance / (primary_distance * 1.0)
        secondary_speed = speed * primary_to_secondary_ratio
        print("Targets - primary: %d, secondary: %d, ratio: %.2f" % (primary_distance, secondary_distance, primary_to_secondary_ratio))

        primary_encoder.reset()
        secondary_encoder.reset()
        
        controller = PIController(proportional_constant=0.015, integral_constant=0.002)

        # Ensure that the encoder knows which way it is going
        primary_encoder.set_direction(math.copysign(1, speed))
        secondary_encoder.set_direction(math.copysign(1, secondary_speed))

        # start the motors, and start the loop
        print("Setting initial speeds to ",speed,":",secondary_speed)
        
        set_primary(speed)
        set_secondary(secondary_speed)
        while abs(primary_encoder.pulse_count) < abs(primary_distance) or abs(secondary_encoder.pulse_count) < abs(secondary_distance):
            # And sleep a bit before calculating
            sleep(0.02)

            # How far off are we?
            secondary_target = primary_encoder.pulse_count * primary_to_secondary_ratio
            error = secondary_target - secondary_encoder.pulse_count

            # How fast should the motor move to get there?
            adjustment = controller.get_value(error)

            set_secondary(secondary_speed + adjustment)
            secondary_encoder.set_direction(math.copysign(1, secondary_speed+adjustment))
            # Some debug
            print "Primary c:{:.2f} ({:.2f} mm)\tSecondary c:{:.2f} ({:.2f} mm) t:{:.2f} e:{:.2f} s:{:.2f} adjustment: {:.2f}".format(
                primary_encoder.pulse_count, 
                primary_encoder.distance_in_mm(),
                secondary_encoder.pulse_count,
                secondary_encoder.distance_in_mm(),
                secondary_target,
                error,
                secondary_speed,
                adjustment
            )

            # Stop the primary if we need to
            if abs(primary_encoder.pulse_count) >= abs(primary_distance):
                print "primary stop"
                set_primary(0)
                secondary_speed = 0

    def drive_arc(self, turn_in_degrees, radius, speed=0.75):
        """ Turn is based on change in heading. """
        # Get the bot width in ticks
        half_width_ticks = EncoderCounter.mm_to_ticks(self.wheel_distance_mm/2.0)
        if turn_in_degrees < 0:
            left_radius     = radius - half_width_ticks
            right_radius    = radius + half_width_ticks
        else:
            left_radius     = radius + half_width_ticks
            right_radius    = radius - half_width_ticks
        print "Arc left radius {:.2f}, right_radius {:.2f}".format(left_radius, right_radius)
        radians = math.radians(abs(turn_in_degrees))
        left_distance = int(left_radius * radians)
        right_distance = int(right_radius * radians)
        print "Arc left distance {}, right_distance {}".format(left_distance, right_distance)
        self.drive_distances(left_distance, right_distance, speed=speed)

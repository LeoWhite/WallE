"""Object for the VL53L1X distance sensor type."""
import atexit
import VL53L1X
import time

class DistanceSensor(object):
    """Represents a distance sensor."""
    def __init__(self):
        # Setup the library
        self._tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self._tof.open()
        self._tof.start_ranging(1)
        
        # Register shutdown call to tidy up
        atexit.register(self.shutdown)

    def shutdown(self):
        self._tof.stop_ranging()

    def get_distance(self):
        """Method to read in the distance"""
        distance = self._tof.get_distance()
        
        # If the distance is greater than max, then the sensor can return a 0 result
        if distance < 50:
          distance = 1000

        return distance

if __name__ == '__main__': 
  ds = DistanceSensor()
  while True:
    print("Distance ", ds.get_distance())
    time.sleep(0.1)
    
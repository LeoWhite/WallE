from WallE import WallE
from time import sleep


class ObstacleAvoidingBehavior(object):
    """Better obstacle avoiding"""
    def __init__(self, WallE):
        self._WallE = WallE

        self.max_distance = 100

    def run(self):
        self._WallE.set_left(0.5)
        self._WallE.set_right(0.5)

        while True:
            # Get the sensor readings
            distance = self._WallE.get_distance()

            print("Distances: l", distance)

            if distance < 150:
                self._WallE.set_left(0)
                self._WallE.set_right(0)

            # Wait our delay time
            sleep(0.1)

behavior = ObstacleAvoidingBehavior(WallE())
behavior.run()

from WallE import WallE
from time import sleep


class ObstacleAvoidingBehavior(object):
    """Better obstacle avoiding"""
    def __init__(self, WallE):
        self._WallE = WallE

        self.max_distance = 100

    def get_speeds(self, nearest_distance):
        if nearest_distance > 100:
            nearest_speed = 100
            furthest_speed = 100
            delay = 100
        elif nearest_distance > 50:
            nearest_speed = 100
            furthest_speed = 80
            delay = 100
        elif nearest_distance > 20:
            nearest_speed = 100
            furthest_speed = 60
            delay = 100
        elif nearest_distance > 10:
            nearest_speed = -40
            furthest_speed = -100
            delay = 100
        else: # collison
            nearest_speed = -100
            furthest_speed = -100
            delay = 250
        return nearest_speed, furthest_speed, delay

    def run(self):
        while True:
            # Get the sensor readings
            distance = self._WallE.get_distance()

            # Get speeds for motors from distances
            nearest_speed, furthest_speed, delay = self.get_speeds(distance)
            print("Distances: l", distance, "Speeds: n", nearest_speed, "f", furthest_speed,
                "Delays: l", delay)

            # Send this to the motors
            #self._WallE.set_left(nearest_speed)
            #self._WallE.set_right(furthest_speed)

            # Wait our delay time
            sleep(delay * 0.001)

behavior = ObstacleAvoidingBehavior(WallE())
behavior.run()
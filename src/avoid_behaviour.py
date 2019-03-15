from WallE import WallE
from time import sleep


class ObstacleAvoidingBehavior(object):
    """Better obstacle avoiding"""
    def __init__(self, WallE):
        self._WallE = WallE

        self.max_distance = 100

    def get_speeds(self, nearest_distance):
        if nearest_distance > 500:
            nearest_speed = 0.75
            furthest_speed = 0.75
            delay = 100
        elif nearest_distance > 450:
            nearest_speed = 0.75
            furthest_speed = 0.5
            delay = 100
        elif nearest_distance > 350:
            nearest_speed = 0.75
            furthest_speed = 0.25
            delay = 100
        elif nearest_distance > 150:
            nearest_speed = 0.6
            furthest_speed = -0.6
            delay = 100
        else: # collison
            nearest_speed = -0.75
            furthest_speed = -0.75
            delay = 250
        return nearest_speed, furthest_speed, delay

    def run(self):
        # Sleep for a second to allow the distance sensor to settle down
        sleep(1)
        
        while True:
            # Get the sensor readings
            distance = self._WallE.get_distance()

            # Get speeds for motors from distances
            nearest_speed, furthest_speed, delay = self.get_speeds(distance)
            print("Distances: l", distance, "Speeds: n", nearest_speed, "f", furthest_speed,
                "Delays: l", delay)

            # Send this to the motors
            self._WallE.set_left(nearest_speed)
            self._WallE.set_right(furthest_speed)

            # Wait our delay time
            sleep(0.1)

behavior = ObstacleAvoidingBehavior(WallE())
behavior.run()
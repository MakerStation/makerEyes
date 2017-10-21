import unittest
import MathUtility
import DataLogger
from functools import partial
import operator
#import math
#from DataLogger import coordinate, sound_speed

class TestDataLogger(unittest.TestCase):

    # def test_coordinate(self):
    #     I = coordinate((2, 3), (38, 17, 30))
    #     self.assertEqual(I, (3, 2, 5))
    #     II = coordinate((2, 3), (70, 61, 50))
    #     self.assertEqual(II, (6, 5, 3))
    #     III = coordinate((4, 1), (38, 29, 30))
    #     self.assertEqual(III, (3, 2, 5))
    #     VI = coordinate((1, 1), (43, 50, 38))
    #     self.assertEqual(VI, (3, 5, -3))
    #
    #
    # def test_soundspeed(self):
    #     cI = sound_speed(20, 101000, 50)
    #     self.assertEqual(cI, 343.99)



    def test_trilateration(self):
        temperature = 20;
        pressure = 101000;
        relativeHumidity = 50;
        soundSpeed = DataLogger.sound_speed(temperature, pressure, relativeHumidity)

        sensorPositions = ((0.0, 0.0, 0.0), (0.4, 0.0, 0.0), (0.0, 0.4, 0.0))
        position = (1.0, 1.0, 1.0)
        distances = tuple(map(partial(MathUtility.distance, position), sensorPositions))
        responseTimes = tuple(map(partial(operator.mul, 1 / soundSpeed), distances))

        distances2 = tuple(map(partial(operator.mul, soundSpeed), responseTimes))
        position2 = MathUtility.normalizedTrilateration(sensorPositions[1][0], sensorPositions[2][0], sensorPositions[2][1], distances2)

        self.assertAlmostEqual(distances, distances2)
        self.assertAlmostEqual(position, position2)



if __name__ == '__main__':
    unittest.main()
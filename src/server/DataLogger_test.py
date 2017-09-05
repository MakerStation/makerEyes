import unittest
#import math
from DataLogger import coordinate, sound_speed

class TestDataLogger(unittest.TestCase):

    def test_coordinate(self):
        I = coordinate((2, 3), (38, 17, 30))
        self.assertEqual(I, (3, 2, 5))
        II = coordinate((2, 3), (70, 61, 50))
        self.assertEqual(II, (6, 5, 3))
        III = coordinate((4, 1), (38, 29, 30))
        self.assertEqual(III, (3, 2, 5))
        VI = coordinate((1, 1), (43, 50, 38))
        self.assertEqual(VI, (3, 5, -3))


    def test_soundspeed(self):
        cI = sound_speed(20, 101000, 50)
        self.assertEqual(cI, 343.99)

if __name__ == '__main__':
    unittest.main()
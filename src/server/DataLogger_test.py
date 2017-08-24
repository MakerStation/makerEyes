import unittest
#import math
from DataLogger import coordinate

class TestDataLogger(unittest.TestCase):

    def test_coordinate(self):
        coordinates = coordinate(2, 3, 38, 17, 30)
        self.assertEqual(coordinates, (3, 2, 5))

if __name__ == '__main__':
    unittest.main()
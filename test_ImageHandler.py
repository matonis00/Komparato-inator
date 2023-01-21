import unittest
from ImageHandler import ImageHandler
import Metrics
import os

class Test_test_ImageHandler(unittest.TestCase):
    def test_findUndefinedPaths(self):

        ih = ImageHandler([],[],[],Metrics.MetricI())

        imageList = list()
        imageList.append(str(os.path.abspath('img\\boat1.jpg')));
        imageList.append(str(os.path.abspath('img\\boat2.jpg')));

        emptyDict = dict()

        result = ih.findUndefinedPaths(imageList, emptyDict)

        self.assertEqual(result, imageList)


if __name__ == '__main__':
    unittest.main()

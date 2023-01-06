import unittest
import Metrics
import os

class Test_test_Metrics(unittest.TestCase):
    def testMethricObject(self):

        obj = Metrics.Object();

        imageList = list()

        imageList.append('C:\\Users\\Jakub\\Desktop\\IO\\komparato-inator\\img\\bananas.jpg');
        imageList.append('C:\\Users\\Jakub\\Desktop\\IO\\komparato-inator\\img\\dog.jpg');
        imageList.append('C:\\Users\\Jakub\\Desktop\\IO\\komparato-inator\\img\\personAndTie.jpg');

        result = obj.group(imageList)

        self.assertTrue(os.path.abspath('img\\bananas.jpg') in result.get('banana')) 
        self.assertTrue(os.path.abspath('img\\dog.jpg') in result.get('dog')) 
        self.assertTrue(os.path.abspath('img\\personAndTie.jpg') in result.get('tie')) 
        self.assertTrue(os.path.abspath('img\\personAndTie.jpg') in result.get('person')) 


        #self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()

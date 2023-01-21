import unittest
import Metrics
import os

class Test_test_Metrics(unittest.TestCase):
    def testMethricObject(self):

        obj = Metrics.Object();

        imageList = list()

        imageList.append(str(os.path.abspath('img\\airplane1.jpg')));
        imageList.append(str(os.path.abspath('img\\airplane2.jpg')));
        imageList.append(str(os.path.abspath('img\\bananas.jpg')));
        imageList.append(str(os.path.abspath('img\\bicycleAndCar.jpg')));
        imageList.append(str(os.path.abspath('img\\bicycleAndPerson.jpg')));
        imageList.append(str(os.path.abspath('img\\bird1.jpg')));
        imageList.append(str(os.path.abspath('img\\bird2.jpg')));
        imageList.append(str(os.path.abspath('img\\boat1.jpg')));
        imageList.append(str(os.path.abspath('img\\boat2.jpg')));
        imageList.append(str(os.path.abspath('img\\bus1.jpg')));
        imageList.append(str(os.path.abspath('img\\bus2.jpg')));
        imageList.append(str(os.path.abspath('img\\car1.jpg')));
        imageList.append(str(os.path.abspath('img\\car2.jpg')));
        imageList.append(str(os.path.abspath('img\\cow1.jpg')));
        imageList.append(str(os.path.abspath('img\\cow2.jpg')));
        imageList.append(str(os.path.abspath('img\\dog1.jpg')));
        imageList.append(str(os.path.abspath('img\\dog2.jpg')));
        imageList.append(str(os.path.abspath('img\\horse1.jpg')));
        imageList.append(str(os.path.abspath('img\\horse2.jpg')));
        imageList.append(str(os.path.abspath('img\\motorcycle1.jpg')));
        imageList.append(str(os.path.abspath('img\\motorcycle2.jpg')));
        imageList.append(str(os.path.abspath('img\\personAndDog.jpg')));
        imageList.append(str(os.path.abspath('img\\personAndTie.jpg')));
        imageList.append(str(os.path.abspath('img\\sheep1.jpg')));
        imageList.append(str(os.path.abspath('img\\sheep2.jpg')));
        imageList.append(str(os.path.abspath('img\\train1.jpg')));
        imageList.append(str(os.path.abspath('img\\train2.jpg')));
        imageList.append(str(os.path.abspath('img\\truck2.jpg')));
        imageList.append(str(os.path.abspath('img\\truck2.jpg')));

        result = obj.group(imageList)

        self.assertTrue(os.path.abspath('img\\airplane1.jpg')in result.get('airplane'));
        self.assertTrue(os.path.abspath('img\\airplane2.jpg')in result.get('airplane'));
        self.assertTrue(os.path.abspath('img\\bananas.jpg')in result.get('banana'));
        self.assertTrue(os.path.abspath('img\\bicycleAndCar.jpg')in result.get('bicycle'));
        self.assertTrue(os.path.abspath('img\\bicycleAndCar.jpg')in result.get('car'));
        self.assertTrue(os.path.abspath('img\\bicycleAndPerson.jpg')in result.get('bicycle'));
        self.assertTrue(os.path.abspath('img\\bicycleAndPerson.jpg')in result.get('person'));
        self.assertTrue(os.path.abspath('img\\bird1.jpg')in result.get('bird'));
        self.assertTrue(os.path.abspath('img\\bird2.jpg')in result.get('bird'));
        self.assertTrue(os.path.abspath('img\\boat1.jpg')in result.get('boat'));
        self.assertTrue(os.path.abspath('img\\boat2.jpg')in result.get('boat'));
        self.assertTrue(os.path.abspath('img\\bus1.jpg')in result.get('bus'));
        self.assertTrue(os.path.abspath('img\\bus2.jpg')in result.get('bus'));
        self.assertTrue(os.path.abspath('img\\car1.jpg')in result.get('car'));
        self.assertTrue(os.path.abspath('img\\car2.jpg')in result.get('car'));
        self.assertTrue(os.path.abspath('img\\cow1.jpg')in result.get('cow'));
        self.assertTrue(os.path.abspath('img\\cow2.jpg')in result.get('cow'));
        self.assertTrue(os.path.abspath('img\\dog1.jpg')in result.get('dog'));
        self.assertTrue(os.path.abspath('img\\dog2.jpg')in result.get('dog'));
        self.assertTrue(os.path.abspath('img\\horse1.jpg')in result.get('horse'));
        self.assertTrue(os.path.abspath('img\\horse2.jpg')in result.get('horse'));
        self.assertTrue(os.path.abspath('img\\motorcycle1.jpg')in result.get('motorcycle'));
        self.assertTrue(os.path.abspath('img\\motorcycle2.jpg')in result.get('motorcycle'));
        self.assertTrue(os.path.abspath('img\\personAndDog.jpg')in result.get('person'));
        self.assertTrue(os.path.abspath('img\\personAndDog.jpg')in result.get('dog'));
        self.assertTrue(os.path.abspath('img\\personAndTie.jpg')in result.get('person'));
        self.assertTrue(os.path.abspath('img\\personAndTie.jpg')in result.get('tie'));
        self.assertTrue(os.path.abspath('img\\sheep1.jpg')in result.get('sheep'));
        self.assertTrue(os.path.abspath('img\\sheep2.jpg')in result.get('sheep'));
        self.assertTrue(os.path.abspath('img\\train1.jpg')in result.get('train'));
        self.assertTrue(os.path.abspath('img\\train2.jpg')in result.get('train'));
        self.assertTrue(os.path.abspath('img\\truck2.jpg')in result.get('truck'));
        self.assertTrue(os.path.abspath('img\\truck2.jpg')in result.get('truck'));

    def testMethricIdentity(self):

        obj = Metrics.Identity();

        imageList = list()

        imageList.append(str(os.path.abspath('similar\\cat1.jpg')));
        imageList.append(str(os.path.abspath('similar\\cat2.png')));
        imageList.append(str(os.path.abspath('similar\\cat3.jpg')));
        imageList.append(str(os.path.abspath('similar\\cow1.jpg')));
        imageList.append(str(os.path.abspath('similar\\dog1.jpg')));
        imageList.append(str(os.path.abspath('similar\\dog2.jpg')));
        imageList.append(str(os.path.abspath('similar\\lcd1.jpg')));

        result = obj.group(imageList)

        catSet = {str(os.path.abspath('similar\\cat1.jpg')), 
                  str(os.path.abspath('similar\\cat2.png')), 
                  str(os.path.abspath('similar\\cat3.jpg')),
                  str(os.path.abspath('similar\\dog2.jpg'))}

        dogSet = {str(os.path.abspath('similar\\dog1.jpg')),
                  str(os.path.abspath('similar\\dog2.jpg'))}

        foundGroups = 0
        for key in result:
            tempSet = set(result.get(key))
            if tempSet == catSet or tempSet == dogSet:
                foundGroups = foundGroups + 1
        
        self.assertEqual(foundGroups, 2);


if __name__ == '__main__':
    unittest.main()

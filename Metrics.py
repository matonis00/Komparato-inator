import imageai
from imageai.Detection import ObjectDetection
import cv2
import os
import glob
import builtins
from typing import List
import imageio.v3 as iio
import numpy as np
import skimage.color
import skimage.util
import matplotlib.pyplot as plt
import image_similarity_measures
from image_similarity_measures.quality_metrics import ssim


class MetricI():
    
    def __init__(self):
        self.metricName=""


    def group(self, pathsList:List[str]):
        pass


class ColorHistogram(MetricI):
    def __init__(self):
        self.metricName="Color"
        print("Utworzono metryke histogramu kolorow")

    def drawHistogram(self):
        image = iio.imread(uri="img\dog2.jpg")
        

        #TODO: CLEAR OR REFAKTOR
        # display the image
        fig, ax = plt.subplots()
        plt.imshow(image)
        # tuple to select colors of each channel line
        colors = ("red", "green", "blue")
        
        # create the histogram plot, with three lines, one for
        # each color
        plt.figure()
        plt.xlim([0, 256])
        for channel_id, color in enumerate(colors):
            histogram, bin_edges = np.histogram(image[:, :, channel_id], bins=256, range=(0, 256))
            plt.plot(bin_edges[0:-1], histogram, color=color)
            
        
        plt.title("Color Histogram")
        plt.xlabel("Color value")
        plt.ylabel("Pixel count")
        
        plt.show()
   


class Object(MetricI):
    
    def __init__(self):
        self.metricName="Obiekty"
        print("Utworzono metryke obiektów")
    
    def group(self, pathsList)->dict:
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.abspath("resnet50_coco_best_v2.1.0.h5"))
        detector.loadModel()
        groupedDict = dict()

        for filename in pathsList:
            imagePath = os.path.abspath(filename)
            detections = detector.detectObjectsFromImage(input_image=imagePath, output_image_path=imagePath, minimum_percentage_probability=60,display_percentage_probability=False, display_object_name=False,
                               display_box=False)

            for eachObject in detections:
                objectName = eachObject["name"]

                if(groupedDict.get(objectName) == None):
                    pathsList = list()
                    pathsList.append(imagePath)
                    groupedDict.update({objectName: pathsList})
                else:
                    listOfItems = groupedDict.get(objectName)
                    if(listOfItems[len(listOfItems)-1]!=imagePath):
                        listOfItems.append(imagePath)
                        groupedDict.update({objectName: listOfItems})
       
        return groupedDict




class Identity(MetricI):
    def __init__(self):
        self.metricName="Podobieńtwo"
        print("Utworzono metryke podobieństwa")

    def group(self, pathsList)->dict:

        groupNumber = 1
        minSimilarity = 0.85
        resultDict = dict()
        foundImages = set()

        for filename in pathsList: 
            test_img = cv2.imread(filename)
        
            ssim_measures = {}
        
            scale_percent = 100 # percent of original img size
            width = int(test_img.shape[1] * scale_percent / 100)
            height = int(test_img.shape[0] * scale_percent / 100)
            dim = (width, height)
        
            for img_path in pathsList:
                if img_path != filename:
                    if img_path not in foundImages:
                        data_img = cv2.imread(img_path)
                        resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
                        ssim_measures[img_path] = ssim(test_img, resized_img)
            
            similar = list()

            for key, value in ssim_measures.items():
                if (value > minSimilarity):
                    similar.append(key)
                    foundImages.add(key)

                    
            if len(similar) != 0:
                name = "Group No."+str(groupNumber)
                similar.append(filename)
                resultDict.update({name: similar})
                foundImages.add(filename)
                groupNumber = groupNumber + 1
        return resultDict
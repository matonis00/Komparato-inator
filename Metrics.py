from dataclasses import dataclass
from imageai.Detection import ObjectDetection
import os
import glob
import builtins

#color histogram imports
import imageio.v3 as iio
import numpy as np
import skimage.color
import skimage.util
import matplotlib.pyplot as plt


@dataclass
class MetricI():
    
    def group(self, listOfPaths):
        pass

@dataclass
class ColorHistogram(MetricI):
    def __init__(self):
        
        print("Utworzono metryke histogramu kolorow")

    def drawHistogram(self):
        image = iio.imread(uri="img\dog2.jpg")
        
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
   


@dataclass
class Object(MetricI):
    
    def __init__(self):
        
        print("Utworzono metryke obiektów")
    
    def group(self, listOfPaths)->dict:
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.abspath("resnet50_coco_best_v2.1.0.h5"))
        detector.loadModel()

        directoryOut = os.path.abspath("newImages")

        listaStringow = listOfPaths

        result = dict()

        for filename in listOfPaths:
            imagePath = os.path.abspath(filename)
            #if os.path.isfile(imagePath):
            detections = detector.detectObjectsFromImage(input_image=imagePath, output_image_path=imagePath, minimum_percentage_probability=60,display_percentage_probability=False, display_object_name=False,
                               display_box=False)

            for eachObject in detections:
                objectName = eachObject["name"]

                if(result.get(objectName) == None):
                    tempList = list()
                    tempList.append(imagePath)
                    result.update({objectName: tempList})
                else:
                    listOfItems = result.get(objectName)
                    if(listOfItems[len(listOfItems)-1]!=imagePath):
                        listOfItems.append(imagePath)
                        result.update({objectName: listOfItems})
        print(result)
        return result



@dataclass
class Identity(MetricI):
    pass


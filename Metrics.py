from imageai.Detection import ObjectDetection
import os
import glob
import builtins

from typing import List


class MetricI():
    
    def __init__(self):
        self.metricName=""
        self.listOfPaths=[]
        self.metricName=""


    def group(self, listOfPaths:List[str]):
        pass

class ColorHistogram(MetricI):
    pass


class Object(MetricI):
    
    def __init__(self):
        self.metricName="Object"
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




class Identity(MetricI):
    pass


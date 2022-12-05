from dataclasses import dataclass
from imageai.Detection import ObjectDetection
import os
import glob
import builtins


@dataclass
class MetricI():
    
    def group():
        pass

@dataclass
class ColorHistogram(MetricI):
    pass


@dataclass
class Object(MetricI):
    
    def __init__(self):
        
        print("Utworzono metryke obiektów")
    #tu bede pisał wykrywanie obiketów
    def group(self, listOfPaths):
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.abspath("resnet50_coco_best_v2.1.0.h5"))
        detector.loadModel()

        directoryOut = os.path.abspath("newImages")

        listaStringow = listOfPaths

        result = dict()

        for filename in listaStringow:
            imagePath = os.path.abspath(filename)
            outputPath = os.path.join(directoryOut, filename)
            if os.path.isfile(imagePath):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    detections = detector.detectObjectsFromImage(input_image=imagePath, output_image_path=outputPath, minimum_percentage_probability=60)

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


    pass


@dataclass
class Identity(MetricI):
    pass


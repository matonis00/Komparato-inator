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
    
    #def __init__(self):   
    def group(self, listOfPaths):
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.abspath("resnet50_coco_best_v2.1.0.h5"))
        detector.loadModel()

        directoryIn = os.path.abspath("images")
        directoryOut = os.path.abspath("newImages")

        listaStringow = listOfPaths
        #listaStringow = list(("image1.jpg", "image2.jpg"))

        result = dict()

        for filename in listaStringow:
            imagePath = os.path.join(directoryIn, filename)
            outputPath = os.path.join(directoryOut, filename)
            if os.path.isfile(imagePath):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    detections = detector.detectObjectsFromImage(input_image=imagePath, output_image_path=outputPath, minimum_percentage_probability=60)
                    #print(imagePath)
                    for eachObject in detections:
                        print(eachObject["name"], " : ", eachObject["percentage_probability"])
                        if(result.get(eachObject["name"]) == None):
                            tempList = list()
                            tempList.append(imagePath)
                            result.update({eachObject["name"]: tempList})
                        else:
                            
                            listOfItems = result.get(eachObject["name"])
                            if(listOfItems[len(listOfItems)-1]!=imagePath):
                                listOfItems.append(imagePath)
                                result.update({eachObject["name"]: listOfItems})

        print(result)


    pass


@dataclass
class Identity(MetricI):
    pass


from typing import List
from dataclasses import dataclass
from Annotation import Annotation
from Metrics import MetricI
import os


@dataclass
class ImageHandler():
    __paths:List[str] 
    __annotations:List[Annotation]
    metric:MetricI



    def scan():
        pass

    #should save results to __paths i suppouse
    def group(self, tempList)->dict:
        return self.metric.group(tempList)
    
    def getAnnotationsList(self)->List[Annotation]:
        return self.__annotations

    def createAnnotationFromScratch(self, imgPath:str, annotationList:List[str]):
        self.__annotations.append(Annotation(imgPath,annotationList))
    

    def createAnnotation(self,annotation:Annotation):
        self.__annotations.append(annotation)


    def loadAnnotationsFromConf(self, annotationsList:List[Annotation]):
        for annotation in annotationsList:
            self.createAnnotation(annotation)


    def userSelectedItem(self, imagePath)->List[str]:
        return self.findEntries(imagePath)

    def getPathAt(self, index:int)->str:
        return self.__paths[index]


    def findEntries(self, imagePath)->List[str]:
        packetStr = [os.path.basename(imagePath)]
        self.__paths = [imagePath]
        for annotation in self.__annotations:
            if(annotation.imagePath == imagePath):
                for path in annotation.content:
                    packetStr += [os.path.basename(path)]
                self.__paths+=annotation.content
                return packetStr
        return packetStr

    def userSavedAnnotation(self, outputPath:str, selectedImage:str)->List[Annotation]:
        found = False
        for annotation in self.__annotations:
            if(annotation.imagePath == selectedImage):
                for path in annotation.content:
                    if(path==outputPath):
                        found = True
                        break
                if(found == False):
                   annotation.content.append(outputPath)
                return self.__annotations
        self.createAnnotationFromScratch(selectedImage,[outputPath])
        return self.__annotations


    def removeAnotation(self,annotationId:int):
        self.__annotations.pop(annotationId)


    #Set some metrics
    def setMetric(self, metric:MetricI)->bool: #Return True if 
        try:
            self.metric=metric
            return True #Notify user if process ended corectly
        except :
            return False #Notify user if process ended incorectly
        



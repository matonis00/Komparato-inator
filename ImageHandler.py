from __future__ import annotations
from typing import List
from dataclasses import dataclass
from Anotation import Anotation
from Metrics import MetricI


@dataclass
class ImageHandler():
    __paths:List[str] 
    __annotations:List[Anotation]
    metric:MetricI


    def __init__(self):
        pass


    def scan():
        pass

    #should save results to __paths i suppouse
    def group():
       pass


    def createAnotation(self,imgPath:str,annotation:str):
        self.__annotations.append(Anotation(imgPath,annotation))


    def removeAnotation(self,annotationId:int):
        self.__annotations.pop(annotationId)


    #Set some metrics
    def setMetric(self, metric:MetricI)->bool: #Return True if 
        try:
            self.metric=metric
            return True #Notify user if process ended corectly
        except :
            return False #Notify user if process ended incorectly
        



from typing import List,Dict,Tuple
from dataclasses import dataclass
from Annotation import Annotation
from ResultSet import ResultSet
from Metrics import MetricI
import os


@dataclass
class ImageHandler():
    __paths:List[str] 
    __annotations:List[Annotation]
    __resultSets:List[ResultSet]
    metric:MetricI


    def scan():
        pass


   


    def validatePaths(self, paths:List[str])->List[str]:
        validPaths = []
        for path in paths:
            if not path.startswith("########"):
                if not path in validPaths:
                    validPaths.append(path)
        return validPaths


    def checkIfAlreadyInMemory(self)->bool:
        for resultSet in self.__resultSets:
            if resultSet.metricName == self.metric.metricName:
                return True


    def loadResultsFromMemory(self, ImagePathList:List[str])->Tuple[Dict[str,List[str]],List[str]]:
        groupedImagesDict={}
        unfoundPaths=[]
        for resultSet in self.__resultSets:
            if resultSet.metricName == self.metric.metricName:
                for lPath in ImagePathList:
                    found = False
                    for key, valueList in resultSet.content.items():
                         if lPath in valueList:
                            if key in groupedImagesDict:
                                groupedImagesDict[key].append(lPath)
                            else:
                                groupedImagesDict[key] = [lPath]
                            found = True
                    if not found:
                        unfoundPaths.append(lPath)
        return groupedImagesDict,unfoundPaths

    def mergeDictionaries(self,firstDict:Dict[str,List[str]], secondDict:Dict[str,List[str]]  )->Dict[str,List[str]]:
        for key, valueList in secondDict.items():
           if key in firstDict:
               firstDict[key] += valueList
           else:
               firstDict[key] = valueList

        return firstDict

    def findUndefinedPaths(self, PathList:List[str], groupedDict:Dict[str,List[str]] )->List[str]:
        unfoundPaths = []
        for path in PathList:
            found = False
            for key, keyList in groupedDict.items():
                if path in keyList:
                    found = True
                    break
            if not found:
                if path not in unfoundPaths:
                    unfoundPaths.append(path)
        return unfoundPaths


    def saveResultSetToMemory(self, resultDict:Dict[str,List[str]]):
        found = False
        for resultSet in self.__resultSets:
            if resultSet.metricName == self.metric.metricName:
                for key, valueList in resultDict.items():
                    if key not in resultSet.content:
                        resultSet.content[key] = valueList
                    else:
                        for value in valueList:
                            if value not in resultSet.content[key]:
                                resultSet.content[key].append(value)
                found = True
                break
        if not found:
            self.appendResultSetFromScratch(self.metric.metricName,resultDict)

    def group(self, imagePathList:List[str])->dict:
        validImagePathList:List[str] = self.validatePaths(imagePathList)
        metricResultFound:bool = self.checkIfAlreadyInMemory()
        if metricResultFound:
            groupedImagesDict, unfoundPaths = self.loadResultsFromMemory(validImagePathList)
            if len(unfoundPaths)==0:
                return groupedImagesDict
            newGroupedImagesDict = self.metric.group(unfoundPaths)
            newGroupedImagesDict = self.mergeDictionaries(newGroupedImagesDict,groupedImagesDict)
        if not metricResultFound:
            newGroupedImagesDict = self.metric.group(validImagePathList)
            unfoundPaths = validImagePathList

        
        undefinedPaths:List[str] = self.findUndefinedPaths(unfoundPaths,newGroupedImagesDict)
        if (len(undefinedPaths)>0):
            if "Undefined" in newGroupedImagesDict:
                newGroupedImagesDict["Undefined"]+=undefinedPaths
            else:
                newGroupedImagesDict["Undefined"]=undefinedPaths
        return newGroupedImagesDict
    
    def appendResultSet(self,newSet:ResultSet):
        self.__resultSets.append(newSet)

    def appendResultSetFromScratch(self,metricName:str, resultSet:Dict[str,List[str]]):
        self.__resultSets.append(ResultSet(metricName,resultSet))

    def getAnnotationsList(self)->List[Annotation]:
        return self.__annotations

    def appendAnnotationFromScratch(self, imgPath:str, annotationList:List[str]):
        self.__annotations.append(Annotation(imgPath,annotationList))
    

    def appendAnnotation(self,annotation:Annotation):
        self.__annotations.append(annotation)

    def userSelectedItem(self, imagePath)->List[str]:
        return self.findEntries(imagePath)

    def getPathAt(self, index:int)->str:
        return self.__paths[index]

    def getAnnotationList(self)->List[Annotation]:
        return self.__annotations

    def getResultsList(self)->List[ResultSet]:
        return self.__resultSets

    def setAnnotationList(self, AnnotationList:List[Annotation]):
        self.__annotations=AnnotationList

    def setResultsList(self,ResultsList:List[ResultSet]):
        self.__resultSets =ResultsList

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
        self.appendAnnotationFromScratch(selectedImage,[outputPath])
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
        



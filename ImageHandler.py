from typing import List,Dict
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
        resultPaths = []
        for path in paths:
            if not path.startswith("########"):
                resultPaths.append(path)
        return resultPaths

    #should save results to __paths i suppouse
    def group(self, pathList:List[str])->dict:
        tempDict={}
        notFoundPaths=[]
        checkedResultSet = False
        pathList = self.validatePaths(pathList)
        ##check if is already in memory
        for resultSet in self.__resultSets:
            if resultSet.metricName == self.metric.metricName:
                checkedResultSet = True
                for lPath in pathList:
                    found = False
                    for key, valueList in resultSet.content.items():
                         if lPath in valueList:
                            if key in tempDict:
                                tempDict[key].append(lPath)
                            else:
                                tempDict[key] = [lPath]
                            found = True
                    if not found:
                        notFoundPaths.append(lPath)

        ##check if is aeverything is categorized                     
        if not checkedResultSet:
            secondDict = self.metric.group(pathList)
        else:
            if len(notFoundPaths)==0:
                return tempDict
            secondDict = self.metric.group(notFoundPaths)

        for key, valueList in secondDict.items():
           if key in tempDict:
               tempDict[key] += valueList
           else:
               tempDict[key] = valueList
        
        ##Check Undefined
        tempPaths = []
        for path in pathList:
            found = False
            for key, keyList in secondDict.items():
                if path in keyList:
                    found = True
                    break
            if not found:
                if path not in tempPaths:
                    tempPaths.append(path)
        if (len(tempPaths)>0):
            tempDict["Undefined"]=tempPaths

        ##Save if necesarry   
        found = False
        for resultSet in self.__resultSets:
            if resultSet.metricName == self.metric.metricName:
                for key, valueList in tempDict.items():
                    if key not in resultSet.content:
                        resultSet.content[key] = valueList
                    else:
                        for value in valueList:
                            if value not in resultSet.content[key]:
                                resultSet.content[key].append(value)
                found = True
                break
        if not found:
            self.createResultSetFromScratch(self.metric.metricName,tempDict)

        return tempDict
    
    def createResultSet(self,newSet:ResultSet):
        self.__resultSets.append(newSet)

    def createResultSetFromScratch(self,metricName:str, resultSet:Dict[str,List[str]]):
        self.__resultSets.append(ResultSet(metricName,resultSet))

    def getAnnotationsList(self)->List[Annotation]:
        return self.__annotations

    def createAnnotationFromScratch(self, imgPath:str, annotationList:List[str]):
        self.__annotations.append(Annotation(imgPath,annotationList))
    

    def createAnnotation(self,annotation:Annotation):
        self.__annotations.append(annotation)


    def loadAnnotationsFromConf(self, annotationsList:List[Annotation]):
        self.__annotations=annotationsList

    def loadResultSetFromConf(self, ResultSets:List[ResultSet]):
        self.__resultSets=ResultSets


    def userSelectedItem(self, imagePath)->List[str]:
        return self.findEntries(imagePath)

    def getPathAt(self, index:int)->str:
        return self.__paths[index]

    def getAnnotationList(self)->List[Annotation]:
        return self.__annotations

    def getResultsList(self)->List[ResultSet]:
        return self.__resultSets

    def setAnnotationList(self, l:List[Annotation]):
        self.__annotations=l

    def setResultsList(self,l:List[ResultSet]):
        self.__resultSets =l

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



    def findResultSet():#TODO
        pass

    def findImageInResultSet():#TODO
        pass

    def addImageToResutSet():#TODO
        pass

    def removeImageFromResultSet():#TODO
        pass



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
        



from typing import List
from dataclasses import dataclass


@dataclass
class ResultSet():#TODO REWORK
    def __init__(self,folderPath, imagePaths:List[str]):
        self.content=[]
        self.folderPath = folderPath
        for path in imagePaths:
            self.content.append(path)


    def addParam(self,contentString:str)->bool:
        self.content.append(contentString)
        return True


    def removeParam(self,contentString:str)->bool:
        self.content.remove(contentString)
        return True


    def removeParam(self,contentId:int)->bool:
        self.content.pop(contentId)
        return True


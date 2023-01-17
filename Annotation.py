from typing import List
from dataclasses import dataclass


@dataclass
class Annotation():
    def __init__(self,imagePath, params:List[str]):
        self.content=[]
        self.imagePath = imagePath
        for param in params:
            self.content.append(param)


    def appendPath(self,path:str)->bool:
        self.content.append(path)
        return True


    def removePathAt(self,path:str)->bool:
        try:
            self.content.remove(path)
            return True
        except ValueError:
            return False


    def removePathAt(self,index:int)->bool:
        try:
            self.content.pop(index)
            return True
        except ValueError:
            return False

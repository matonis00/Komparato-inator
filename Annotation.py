from typing import List
from dataclasses import dataclass, field


@dataclass
class Annotation():
    def __init__(self,imagePath, params:List[str]):
        self.content=[]
        self.imagePath = imagePath
        for param in params:
            self.content.append(param)


    def addParam(self,contentString:str)->bool:
        self.content.append(contentString)
        return True


    def removeParam(self,contentString:str)->bool:
        try:
            self.content.remove(contentString)
            return True
        except ValueError:
            return False


    def removeParam(self,contentId:int)->bool:
        try:
            self.content.pop(contentId)
            return True
        except ValueError:
            return False

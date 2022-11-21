from typing import List
from dataclasses import dataclass


@dataclass
class Anotation():
    imagePath:str
    content:List[str]

    def __init__(self,imagePath,content):
        self.imagePath=imagePath
        self.content.append(content)


    def addContent(self,contentString:str)->bool:
        self.content.append(contentString)
        return True


    def substractContent(self,contentString:str)->bool:
        self.content.remove(contentString)
        return True


    def substractContent(self,contentId:int)->bool:
        self.content.pop(contentId)
        return True



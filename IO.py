from typing import  List
import glob
import os
from Annotation import Annotation

class IO():
    def __init__(self):
        pass

    def loadAnnotations(self):
       fileContent = []
       try:
            plik = open("config/annotations.conf", "r")
            filePath=""
            for linia in plik:
                if linia.startswith("filePath:"):
                    filePath = linia.split("\"")[1].strip()
                elif linia.startswith("annotations:"):
                    params=[]
                    for linia in plik:
                        if linia.startswith("{"):
                            continue
                        if linia.startswith("}"):
                            fileContent.append(Annotation(filePath, params))
                            break
                        params.append(linia.split("\"")[1].strip())
            plik.close()
            return fileContent
       except FileNotFoundError:
            plik = open("config/annotations.conf", "w")
            plik.close()
            return fileContent
        


    def saveAnnotations(self, annots:List[Annotation]):
            plik = open("config/annotations.conf", "w")
            for annotate in annots:
                plik.write("@"+ os.path.basename(annotate.imagePath)+"\n")
                plik.write("filePath: "+"\""+annotate.imagePath+"\"\n")
                plik.write("annotations:\n{\n")
                for param in annotate.content:
                    plik.write(" \""+param+"\"\n")
                plik.write("}\n")    
            plik.close()

    def loadResult():
        pass

    def saveResult():
        pass

    def findEntry(entry:str)->bool:
        pass

    def readPath(self,sourcePath)->list:
        tempList = list()
        for fileName in glob.iglob(sourcePath + '**/**', recursive=True):
            if os.path.isfile(fileName):
                if fileName.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(fileName)
                    #if fileName not in tempList:
                    tempList.append(fileName)
        return tempList





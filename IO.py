from typing import  List
import glob
import os
import pickle
from Annotation import Annotation
from ResultSet import ResultSet
from PyQt5.QtGui import QPixmap

class IO():
    def __init__(self):
        pass

    def loadAnnotationsFromConfFile(self)->List[Annotation]:
       annotationList = []
       try:
            plik = open("config/annotations.conf", "r")
            filePath=""
            for linia in plik:
                if linia.startswith("filePath:"):
                    filePath = linia.split("\"")[1].strip()
                elif linia.startswith("annotations:"):
                    paths=[]
                    for linia in plik:
                        if linia.startswith("{"):
                            continue
                        if linia.startswith("}"):
                            annotationList.append(Annotation(filePath, paths))
                            break
                        paths.append(linia.split("\"")[1].strip())
            plik.close()
            return annotationList
       except FileNotFoundError:
            plik = open("config/annotations.conf", "w")
            plik.close()
            return annotationList
        


    def saveAnnotationsToFile(self, annotations:List[Annotation]):
            plik = open("config/annotations.conf", "w")
            for annotate in annotations:
                plik.write("@"+ os.path.basename(annotate.imagePath)+"\n")
                plik.write("filePath: "+"\""+annotate.imagePath+"\"\n")
                plik.write("annotations:\n{\n")
                for param in annotate.content:
                    plik.write(" \""+param+"\"\n")
                plik.write("}\n")    
            plik.close()


    def serialize(self, serializableObject, destination:str):
        with open(destination, "wb") as f:
            pickle.dump(serializableObject, f)

    def deSerialize(self, source:str):
        with open(source, "rb") as f:
            serializableObject = pickle.load(f)
            return serializableObject

    def exportImage(self, pixmap:QPixmap, format:str)->bool:
        pixmap.save(format);
        return True

    def readPath(self,sourcePath)->list:
        pathsList = list()
        for fileName in glob.iglob(sourcePath + '**/**', recursive=True):
            if os.path.isfile(fileName):
                if fileName.lower().endswith(('.jpg', '.jpeg', '.png')):
                    pathsList.append(fileName)
        return pathsList

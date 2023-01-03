from typing import List
from Annotation import Annotation
from IO import IO
import UserInterface
import Metrics
from ImageHandler import ImageHandler
import numpy as np
import cv2 
import Metrics

class Session():

    def __init__(self):
        self.__isPremium:bool
        self.userInterface = UserInterface.MainUserInterface()
        self.handler:ImageHandler = ImageHandler()
        self.InOut:IO=IO()
        self.userInterface.groupBtn.clicked.connect(self.groupImages)
        self.userInterface.browseBtn.clicked.connect(self.loadPaths)
        self.userInterface.saveAnnotationSignal.connect(self.userSavedAnnotation)
        self.annotationList:List[Annotation] = self.InOut.loadAnnotations()
        self.InOut.saveAnnotations(self.annotationList)





    def userSavedAnnotation(self, outputPath:str):
        saved = False
        for annotation in self.annotationList:
            if(annotation.imagePath == self.userInterface.selectedImage):
                for path in annotation.content:
                    if(path==outputPath):
                        break
                annotation.content.append(outputPath)
                saved = True
                self.InOut.saveAnnotations(self.annotationList)
                break
        if(saved == False):
            self.annotationList.append(Annotation(self.userInterface.selectedImage, [outputPath]))
            self.InOut.saveAnnotations(self.annotationList)


    def __validateKey(self,key) -> bool:
        pass

    def loadPaths(self):
        self.userInterface.GetSource()
        
        #for fileName in glob.iglob(sourcePath + '**/**', recursive=True):
        #    if os.path.isfile(fileName):
        #        if fileName.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        #            print(fileName)
        #            self.tempList.append(fileName)

        self.userInterface.SetupListView(self.InOut.readPath(self.userInterface.sourcePath))


    def getUI(self)->UserInterface.MainUserInterface:
        return self.userInterface

    def groupImages(self ):
        metryka:Metrics.MetricI = Metrics.Object()
        self.handler.setMetric(metryka)

        dictonary = dict()
        dictonary = self.handler.group(self.userInterface.contentList)
        listP = list()

        for key in dictonary.keys():
            listP.append("########"+key+"########")
            listP = listP + dictonary[key]

        self.userInterface.SetupListView(listP)
        #self.userInterface.resutl = self.handler.group(self.userInterface.tempList)

def main():
    app = UserInterface.QApplication(UserInterface.sys.argv)
   # imagePath="nowy.jpg"
    imagePath="CatInHalf.jpg"
    sesja = Session()
    sesja.getUI().show()
    


    UserInterface.sys.exit(app.exec())
    sesja.getUI()    #sesja.getUI().openImageEditWindow(imagePath)

if __name__=='__main__':
        main()

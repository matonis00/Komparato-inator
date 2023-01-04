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
        self.InOut:IO=IO()
        self.handler:ImageHandler = ImageHandler([],[],Metrics.MetricI())
        self.userInterface.groupBtn.clicked.connect(self.groupImages)
        self.userInterface.browseBtn.clicked.connect(self.loadPaths)
        self.userInterface.saveAnnotationSignal.connect(self.userSavedAnnotation)
        self.userInterface.onSelectItemSignal.connect(self.userSelectedItem)
        self.userInterface.annotationComboBox.currentIndexChanged.connect(self.onAnnotationComboBoxChanged)
        self.handler.loadAnnotationsFromConf(self.InOut.loadAnnotations())




    def onAnnotationComboBoxChanged(self, index):
        imagePath = self.userInterface.selectedImage
        if(index > 0):
            annotationPath = self.handler.getPathAt(index)
        else:
            annotationPath=""
        self.userInterface.SetupGraphicViewWithAnnotation(imagePath, annotationPath)


    def userSelectedItem(self, imagePath):
        self.userInterface.LoadImageAnnotations(self.handler.userSelectedItem(imagePath))

    def userSavedAnnotation(self, outputPath:str):
        newList = self.handler.userSavedAnnotation(outputPath ,self.userInterface.selectedImage)
        if(newList.__len__ != 0):   
            self.InOut.saveAnnotations(newList)    
            self.userInterface.LoadImageAnnotations(self.handler.userSelectedItem(self.userInterface.selectedImage))
            


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

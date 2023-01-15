from pickle import NONE
from typing import List
from Annotation import Annotation
from IO import IO
import UserInterface
import Metrics
from ImageHandler import ImageHandler
import numpy as np
import cv2 
import Metrics
import webbrowser

class Session():

    def __init__(self):
        self.__isPremium:bool
        self.userInterface = UserInterface.MainUserInterface()
        self.InOut:IO=IO()
        self.handler:ImageHandler = ImageHandler([],[],[],Metrics.MetricI())
        self.userInterface.groupBtn.clicked.connect(self.groupImages)
        self.userInterface.browseBtn.clicked.connect(self.loadPaths)
        self.userInterface.exportBtn.clicked.connect(self.selectExportPath)
        self.userInterface.saveAnnotationSignal.connect(self.userSavedAnnotation)
        self.userInterface.onSelectItemSignal.connect(self.userSelectedItem)
        self.userInterface.annotationComboBox.currentIndexChanged.connect(self.onAnnotationComboBoxChanged)
        #self.handler.loadAnnotationsFromConf(self.InOut.loadAnnotations())
        try:
            #self.handler.loadAnnotationsFromConf(self.InOut.deSerialize("config\\annotations.conf"))
            self.handler.loadAnnotationsFromConf(self.InOut.loadAnnotations())
        except:
            self.handler.setAnnotationList([])
        try:
            self.handler.loadResultSetFromConf(self.InOut.deSerialize("config\\results.conf"))
        except:
            self.handler.setResultsList([])



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
            #self.InOut.serialize(newList,"config\\annotations.conf")  
            self.InOut.saveAnnotations(newList)
            self.userInterface.LoadImageAnnotations(self.handler.userSelectedItem(self.userInterface.selectedImage))
            


    def __validateKey(self,key) -> bool:
        pass

    def loadPaths(self):
        path = self.userInterface.getPath("Select source path")
        if(path!="" and path): 
            self.userInterface.sourcePath = path.replace('/',"\\")
            self.userInterface.SetupListView(self.InOut.readPath(self.userInterface.sourcePath))
        else:
            self.userInterface.showMessageBox("Select Proper folder")


    def selectExportPath(self):
        if(self.userInterface.selectedImage!=""):
            exportPath = self.userInterface.getSavePath();
            if(exportPath!=""):
                pixmap = self.userInterface.graphicView.pixmap()
                self.InOut.exportImage(pixmap,exportPath)
                
        else:
            self.userInterface.showMessageBox("Select any picture")
        


    def getUI(self)->UserInterface.MainUserInterface:
        return self.userInterface

    def groupImages(self ):
        metryka:Metrics.MetricI = Metrics.Object()
        self.handler.setMetric(metryka)

        dictonary = dict()
        dictonary = self.handler.group(self.userInterface.contentList)
        self.InOut.serialize(self.handler.getResultsList(),"config\\results.conf")

        #testing generating html page with result
        f = open('Result.html', 'w')
        html_template = """
        <html>
        <head>
        <title>Title</title>
        </head>
        <body>
        <h1>RESULTS</h1>
        """
        for key in dictonary.keys():
            html_template +="<h2>"+key+"</h2><div width='100%'>"
            for element in dictonary[key]:
                html_template +="<img src="+element+" alt="+element+" width='200' height='200'>" 
            html_template +="</div>"

        html_template +="""
        </body>
        </html>
        """
        f.write(html_template)
        f.close()
        webbrowser.open('Result.html')
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

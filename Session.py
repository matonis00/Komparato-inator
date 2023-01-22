from typing import List, Dict
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
        self.__metricList:List[Metrics.MetricI]=[]
        
        self.userInterface = UserInterface.MainUserInterface()
        self.InOut:IO=IO()
        self.handler:ImageHandler = ImageHandler([],[],[],Metrics.MetricI())
        self.userInterface.groupBtn.clicked.connect(self.groupImages)
        self.userInterface.browseBtn.clicked.connect(self.loadPaths)
        self.userInterface.exportBtn.clicked.connect(self.selectExportPath)
        self.userInterface.saveAnnotationSignal.connect(self.userSavedAnnotation)
        self.userInterface.onSelectItemSignal.connect(self.userSelectedItem)
        self.userInterface.annotationComboBox.currentIndexChanged.connect(self.onAnnotationComboBoxChanged)
        self.userInterface.metricComboBox.currentIndexChanged.connect(self.onMetricComboBoxChanged)
        try: 
            self.handler.setAnnotationList(self.InOut.loadAnnotationsFromConfFile())
        except:
            self.handler.setAnnotationList([])
        try:
            self.handler.setResultsList(self.InOut.deSerialize("config\\results.conf"))
        except:
            self.handler.setResultsList([])
        self.fillMetricList([Metrics.Identity(),Metrics.Object()])
        self.currentMetricIndex = 0
        self.userInterface.setupMetricsComboBox(self.getMetricNames())


    
    def fillMetricList(self,metricList:List[Metrics.MetricI]):
        for metric in metricList:
            self.__metricList.append(metric)

    def getMetricNames(self)->List[str]:
        metricNames=[]
        for metric in self.__metricList:
            metricNames.append(metric.metricName)
        return metricNames

    def onAnnotationComboBoxChanged(self, index):
        imagePath = self.userInterface.selectedImage
        if(index > 0):
            annotationPath = self.handler.getPathAt(index)
        else:
            annotationPath=""
        self.userInterface.SetupGraphicViewWithAnnotation(imagePath, annotationPath)

    def onMetricComboBoxChanged(self, index):
        self.currentMetricIndex = index
    

    def userSelectedItem(self, imagePath):
        self.userInterface.LoadImageAnnotations(self.handler.userSelectedItem(imagePath))


    def userSavedAnnotation(self, outputPath:str):
        newList = self.handler.userSavedAnnotation(outputPath, self.userInterface.selectedImage)
        if(newList.__len__ != 0):   
            self.InOut.saveAnnotationsToFile(newList)
            self.userInterface.LoadImageAnnotations(self.handler.userSelectedItem(self.userInterface.selectedImage))
            


    def __validateKey(self,key) -> bool:
        pass


    def loadPaths(self):
        path = self.userInterface.getPath("Select source path")
        if(path!="" and path): 
            self.userInterface.sourcePath = path.replace('/',"\\")
            self.userInterface.SetupListView(self.InOut.readPath(self.userInterface.sourcePath))
            self.userInterface.BrowseBtnClicked()
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

    def createWebView(self, GroupedImagesDict:Dict[str,List[str]]):
        f = open('Result.html', 'w')
        html_template = """
        <html>
        <head>
        <style>
             @font-face {
                font-family:'Montserrat';
                src: URL('font/Montserrat-VariableFont_wght.ttf') format('truetype');
                }
            img {
                width: 100%;
                height: auto;
                display: block;
                margin-bottom: 20px;
                padding: 10px;
                background: #ffeefe;
                box-shadow: 0 0 5px rgb(0, 0, 0, .9);
                box-sizing: border-box;
            }


            .container {
                column-count: 3;
                max-width: 1000px;
                margin: 0 auto;
                background: #263a96;
                padding: 30px;
                box-shadow: 10px 10px 8px #ACC2FF;
                border-radius: 00px 0px 30px 30px;
            }


            h1 {
                padding-top: 30px;
                font-family: Montserrat;
                color: #fefefe;
                text-align:center;

            }
            h2 {
                font-family: Montserrat;
                color: #fefefe;
                margin-top: 100px;
                margin-bottom: 0;
                border-radius: 30px 30px 0px 0px;
                margin-left: auto;
                margin-right: auto;
                text-align: center;
                background: #263a96;
                max-width: 1000px;
                padding: 30px;
                box-shadow: 10px 13px 8px #ACC2FF;
            }
                h2:first-letter {
                    text-transform: uppercase;
                }
            body {
                background: rgb(255,238,255);
                background: linear-gradient(90deg, rgba(255,238,255,1) 0%, rgba(243,233,231,1) 100%);
            }
        </style>
        <title>Wynik Grupowania</title>
        <title>Komparato-inator</title>
        </head>
        <body>
        <div width = "100%">
        """
        for key in GroupedImagesDict.keys():
            html_template +="<h2>"+key+"</h2>"
            html_template +="""
            <div class="container">
            """
            for element in GroupedImagesDict[key]:
                html_template +="<img src=\""+element+"\" >" 
            html_template +="""
            </div>
            """

        html_template +="""
        </div>
        </body>
        </html>
        """
        f.write(html_template)
        f.close()
        return True




    def groupImages(self ):
        
        self.handler.setMetric(self.__metricList[self.currentMetricIndex])
        GroupedImagesDict:Dict[str,List[str]] = self.handler.group(self.userInterface.contentList)
        self.handler.saveResultSetToMemory(GroupedImagesDict)
        self.InOut.serialize(self.handler.getResultsList(),"config\\results.conf")

        self.createWebView(GroupedImagesDict)
        webbrowser.open('Result.html')
        imagesList:List[str] = []

        for key in GroupedImagesDict.keys():
            imagesList.append("########"+key+"########")
            imagesList = imagesList + GroupedImagesDict[key]
        
        self.userInterface.SetupListView(imagesList)

def main():
    app = UserInterface.QApplication(UserInterface.sys.argv)
    sesja = Session()
    sesja.getUI().show()
    


    UserInterface.sys.exit(app.exec())
    sesja.getUI()    #sesja.getUI().openImageEditWindow(imagePath)

if __name__=='__main__':
        main()

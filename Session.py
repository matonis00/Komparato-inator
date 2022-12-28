from dataclasses import dataclass
from IO import IO
import UserInterface
from ImageHandler import ImageHandler
import numpy as np
import cv2 
from PySide6.QtUiTools import QUiLoader
import Metrics

class Session():

    def __init__(self):
        self.__isPremium:bool
        self.userInterface = UserInterface.MainUserInterface()
        self.handler:ImageHandler = ImageHandler()
        self.InOut:IO=IO()
        self.userInterface.groupBtn.clicked.connect(self.groupImages)

    def __validateKey(self,key) -> bool:
        pass


    def getUI(self)->UserInterface.MainUserInterface:
        return self.userInterface

    def groupImages():
        metryka:MetricI = Metrics.Object()
        self.handler.setMetric(metryka)
        print(self.handler.group(self.userInterface.tempList))
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
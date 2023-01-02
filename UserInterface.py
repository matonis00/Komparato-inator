from dataclasses import dataclass
import math
from msilib.schema import File
from typing import List

#from PySide6.QtWidgets import QApplication, QDialog , QDialogButtonBox, QVBoxLayout, QLineEdit, QMainWindow, QPushButton
#from PySide6.QtUiTools import QUiLoader
#from PySide6.QtCore import QFile, QIODevice, QObject

from PyQt5.QtWidgets import QApplication, QAbstractItemView, QDialog, QLabel, QDialogButtonBox, QVBoxLayout, QLineEdit, QMainWindow, QPushButton, QListView, QGraphicsView,QComboBox, QFileDialog
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
import numpy as np
import os
import glob
import sys
import cv2 

import Metrics

class DialogBox(QDialog):
    firstTime = True

    def __init__(self, parent=None):
        self.text=""
        super(DialogBox, self).__init__()
        self.lineInput = QLineEdit()
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addWidget(self.lineInput)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.setWindowTitle("Enter Annotation comment")

    def accept(self) -> None:
        self.text=self.lineInput.text()
        self.lineInput.setText("")
        return super().accept()

    def reject(self) -> None:
        self.text=""
        self.lineInput.setText("")
        return super().reject()
    def printText(self):
        return self.text
        
        

class MainUserInterface(QMainWindow):
    tempList = list()
    resutl= dict()
    global ListViewModel, selectedImage
    selectedImage = "" #PlaceHolder!!! should be replaced with proper verivication
    ListViewModel = QtGui.QStandardItemModel()


    def __init__(self,UIFilePath:str="./UIFiles/form.ui"):
        super(MainUserInterface,self).__init__()
        loadUi(UIFilePath,self)
        self.sourcePath = ""
        self.Dbox=DialogBox()
        self.annotateBtn = self.findChild(QPushButton,"adnoteButton")
        self.groupBtn = self.findChild(QPushButton,"groupButton")
        self.browseBtn = self.findChild(QPushButton,"browseButton")
        self.metricComboBox = self.findChild(QComboBox,"comboBox")
        self.annotationComboBox = self.findChild(QComboBox,"comboBox_2")
        self.listView = self.findChild(QListView,"listView")
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.graphicView = self.findChild(QLabel,"graphicsView")
        self.listView.clicked.connect(self.OnItemSelected)
        self.annotateBtn.clicked.connect(self.OnAnnotateBtnClicked)
        #self.groupBtn.clicked.connect(self.OnGroupBtnClicked) #No Neccesary anymore
        self.browseBtn.clicked.connect(self.OnBrowseBtnClicked)
        self.contentList = list()

        #QlistView Inicialization
        self.listView.setModel(ListViewModel)



    def SetupListView(self, ItemList):
        ListViewModel.clear()
        self.contentList = ItemList
        for elem in ItemList:
            item = QtGui.QStandardItem(os.path.basename(elem))
            ListViewModel.appendRow(item)

    def SetupGraphicView(self, imagePath):
        pixmap = QtGui.QPixmap(imagePath)
        #TODO:
        #ImageWidthLabel = pixmap.width() #I want to print real size
        #ImageHeightLabel pixmap.height() #Need some small labels in UI
        pixmap = pixmap.scaled(471,471)
        self.graphicView.setPixmap(pixmap)


    #On List View Item Selected
    def OnItemSelected(self, index):
        global selectedImage
        if self.contentList[index.row()].lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            selectedImage = str(self.contentList[index.row()])
            self.SetupGraphicView(selectedImage)

        #print ("selected item index found at %s with data: %s" % (index.row(), index.data()))

    def GetSource(self):
        self.sourcePath = QFileDialog.getExistingDirectory(None, 
                                                        'Select images source', 
                                                         QtCore.QDir.rootPath(), 
                                                         QFileDialog.ShowDirsOnly)

    #On Browse Button Clicked
    def OnBrowseBtnClicked(self ):
       # self.tempList = list()
        #self.sourcePath = QFileDialog.getExistingDirectory(None, 
           #                                              'Select images source', 
          #                                               QtCore.QDir.rootPath(), 
         #                                                QFileDialog.ShowDirsOnly)  
        #for fileName in glob.iglob(sourcePath + '**/**', recursive=True):
        #    if os.path.isfile(fileName):
        #        if fileName.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        #            print(fileName)
        #            self.tempList.append(fileName)

        #self.SetupListView(self.tempList)
        #metryka = Metrics.Object()
        #result = metryka.group(tempList)
        print("result")

        #self.SourcePath = sourcePath


    def OnAnnotateBtnClicked(self):
        print(selectedImage);
        if selectedImage != "":
            print(selectedImage);
            self.openImageEditWindow(selectedImage)

    def openImageEditWindow(self,imagePath:str):
        size=2
        global inputImage
        global annotationLayer
        textBox=self.Dbox
        if os.path.exists(imagePath)==False:
            return
            
        inputImage = cv2.imread(imagePath)
        if inputImage.shape[2] == 3:
            b_channel, g_channel, r_channel = cv2.split(inputImage)
            alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
            inputImage = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        tempimageName=os.path.basename(imagePath)
        imageName= tempimageName[ :tempimageName.index(".")]
        annotationLayer = np.zeros((inputImage.shape[0],inputImage.shape[1],4), np.uint8)
        dummyImage=inputImage.copy()
        
        outputImage=imageName+"_annotated.png"
        outputPath="./Annotations/"+outputImage
        i=1
        while(os.path.exists(outputPath)==True):#if exist add number to name
            outputImage=imageName+"_annotated_"+str(i)+".png"
            outputPath="./Annotations/"+outputImage
            i+=1

        handDrawMode = False # true if hand drawing mode is on
        rectangleMode = True # if True, draw rectangle.
        circleMode = False # if True, draw circle.
        borradorMode = False # if True, use Eraser.
        global textMode # if True, draw circle.
        global isDrawing# true if mouse is pressed
        
        textMode ,isDrawing = False, False
        ix,iy =-1,-1
        
        # mouse callback function
        # C - Clear
        # D - Hand draw
        # R - Rectangle
        # E - Circle
        # S - Save
        # ESC - exit

        def draw(event,x,y,flags,param):
            global inputImage
            global annotationLayer
            global ix,iy,InputText
            global isDrawing # true if mouse is pressed
            if event == cv2.EVENT_LBUTTONDOWN:
                isDrawing = True
                ix,iy = x,y
                if textMode == True:
                    text = textBox.printText()#Public probably TO DO: REWORK
                    cv2.putText(inputImage,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0,255),int((size/4)))
                    cv2.putText(annotationLayer,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0,255),int((size/4)))
            elif event == cv2.EVENT_MOUSEMOVE and isDrawing == True:
                if handDrawMode == True:
                    cv2.line(annotationLayer,(ix,iy),(x,y),(0,255,0,255),size)
                    cv2.line(inputImage,(ix,iy),(x,y),(0,255,0,0),size)
                    ix,iy = x,y
                elif borradorMode == True:
                    cv2.line(annotationLayer,(ix,iy),(x,y),(0,0,0,0),size)
                    cv2.line(inputImage,(ix,iy),(x,y),(255,255,255,255),size)
                    ix,iy = x,y

            elif event == cv2.EVENT_LBUTTONUP:
                isDrawing = False
                if rectangleMode == True:
                    cv2.rectangle(annotationLayer,(ix,iy),(x,y),(0,255,0,255),size)
                    cv2.rectangle(inputImage,(ix,iy),(x,y),(0,255,0),size)
                elif circleMode == True:
                    sx=int((ix+x)/2)
                    sy=int((iy+y)/2)
                    truR=int(math.sqrt(math.pow(ix-x,2)+math.pow(iy-y,2))/2)
                    cv2.circle(annotationLayer,(sx,sy),truR,(0,0,255,255),size)
                    cv2.circle(inputImage,(sx,sy),truR,(0,0,255,255),size)
                elif borradorMode == True:
                        inputImage=cv2.addWeighted(annotationLayer,1,dummyImage,1,0)#Smth is inherently wrong. I can't pinpoint it though.
                        


        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw,self.Dbox)
        
        while(1):
            cv2.imshow('image',inputImage)
            #cv2.imshow('adnotation',img2)
            k = cv2.waitKey(1)
            if k == ord('+'):# increase size
                size+=1
                if size>32:
                    size=32
            elif k == ord('-'):# decrease size
                size-=1
                if size<1:
                    size=1
            elif k == ord('t'):#Switch to draw circle
               borradorMode = False
               rectangleMode = False
               circleMode= False
               handDrawMode = False
               textMode = True
               
               textBox.show() #Public probably TO DO: REWORK
               textBox.setGeometry(500,500,200,100) #Public probably TO DO: REWORK
            elif k == ord('t'):#Switch to draw circle
               borradorMode = False
               rectangleMode = False
               circleMode= False
               handDrawMode = False
               textMode = True
               
               textBox.show() #Public probably TO DO: REWORK
               textBox.setGeometry(500,500,200,100) #Public probably TO DO: REWORK
            elif k == ord('b'):#Switch to use borrador
               borradorMode = True
               rectangleMode = False
               circleMode= False
               handDrawMode = False
               textMode = False
            elif k == ord('e'):#Switch to draw Elipse
                borradorMode = False
                rectangleMode = False
                circleMode= True
                handDrawMode = False
                textMode = False
            elif k == ord('d'):#Switch to hand draw
               borradorMode = False
               rectangleMode = False
               circleMode= False
               handDrawMode = True
               textMode = False
            elif k == ord('s'):#saves edits in annotation
               cv2.imwrite(outputPath,annotationLayer)
               cv2.imwrite("./cat.png",inputImage)
            elif k == ord('c'):#Clears with dummy image
               inputImage=dummyImage.copy()
               annotationLayer = np.zeros((inputImage.shape[0],inputImage.shape[1],4), np.uint8)
            elif k == 27:#ESC
               break
            
        cv2.destroyAllWindows()   

        

          






from __future__ import annotations
import math
import string
from PIL import Image, ImageQt
from PyQt5.QtWidgets import QApplication,QMessageBox, QAbstractItemView, QDialog, QLabel, QDialogButtonBox, QVBoxLayout, QLineEdit, QMainWindow, QPushButton, QListView, QGraphicsView,QComboBox, QFileDialog
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
from typing import List
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
    saveAnnotationSignal = QtCore.pyqtSignal(str)
    onSelectItemSignal = QtCore.pyqtSignal(str)
    global ListViewModel
    ListViewModel = QtGui.QStandardItemModel()


    def __init__(self,UIFilePath:str="./UIFiles/form.ui"):
        super(MainUserInterface,self).__init__()
        loadUi(UIFilePath,self)
        self.selectedImage = "" #PlaceHolder!!! should be replaced with proper verivication
        self.sourcePath = ""
        self.imageChoosen = False
        self.folderChoosen = False
        self.Dbox=DialogBox()
        self.annotateBtn = self.findChild(QPushButton,"adnoteButton")
        self.groupBtn = self.findChild(QPushButton,"groupButton")
        self.browseBtn = self.findChild(QPushButton,"browseButton")
        self.exportBtn = self.findChild(QPushButton,"pushButton")
        self.metricComboBox = self.findChild(QComboBox,"comboBox")
        self.annotationComboBox = self.findChild(QComboBox,"comboBox_2")
        self.listView = self.findChild(QListView,"listView")
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.graphicView = self.findChild(QLabel,"graphicsView")
        self.sizeLabel = self.findChild(QLabel,"sizeLabel")
        self.listView.clicked.connect(self.OnItemSelected)
        self.annotateBtn.clicked.connect(self.OnAnnotateBtnClicked)
        #self.groupBtn.clicked.connect(self.OnGroupBtnClicked) #No Neccesary anymore
        self.browseBtn.clicked.connect(self.OnBrowseBtnClicked)
        self.contentList = list()


        #buttons setup
        self.annotateBtn.setEnabled(False)
        self.exportBtn.setEnabled(False)
        self.groupBtn.setEnabled(False)

        #QlistView Inicialization
        self.listView.setModel(ListViewModel)
        #Image visualization Inicialization
        size = QtCore.QSize(471.0,471.0)
        whiteColor = QtGui.QColor(255,255,255)
        whitePixmap = QtGui.QPixmap(size)
        whitePixmap.fill(whiteColor)
        self.graphicView.setPixmap(whitePixmap)
       

        

    def SetupListView(self, ItemList):
        ListViewModel.clear()
        self.contentList = ItemList
        for elem in ItemList:
            item = QtGui.QStandardItem(os.path.basename(elem))
            ListViewModel.appendRow(item)

    def SetupGraphicView(self, imagePath):
        pixmap = QtGui.QPixmap(imagePath)
        imageWidth = pixmap.width() 
        imageHeight = pixmap.height()
        pixmap = pixmap.scaled(471,471)
        self.sizeLabel.setText(str(imageWidth)+"/"+str(imageHeight)+"px")
        self.graphicView.setPixmap(pixmap)


    #On List View Item Selected
    def OnItemSelected(self, index):
        if self.contentList[index.row()].lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            self.selectedImage = str(self.contentList[index.row()])
            self.onSelectItemSignal.emit(self.selectedImage)
            self.SetupGraphicView(self.selectedImage)
            if(self.imageChoosen == False):
                self.annotateBtn.setEnabled(True)
                self.exportBtn.setEnabled(True)
                self.imageChoosen = True



    def LoadImageAnnotations(self, paths:List[str]):
        self.annotationComboBox.clear()
        for path in paths:
            self.annotationComboBox.addItem(path)
        self.annotationComboBox.setCurrentIndex(0)

    def SetupGraphicViewWithAnnotation(self, baseImagePath:str, annotationPath:str):
        try:
            if(annotationPath !=""):
                baseImage = Image.open(baseImagePath)
                annotation = Image.open(annotationPath)
                mode1 = baseImage.mode
                if(str(mode1) == "RGB"):
                    baseImage = baseImage.convert("RGBA")
                baseImage.alpha_composite(annotation)
                pixmap=ImageQt.toqpixmap(baseImage)
                imageWidth = pixmap.width() 
                imageHeight = pixmap.height()
                self.sizeLabel.setText(str(imageWidth)+"/"+str(imageHeight)+"px")
                self.graphicView.setPixmap(pixmap.scaled(471,471))
            else:
                self.SetupGraphicView(baseImagePath)
        except:
             self.SetupGraphicView(baseImagePath)

        #print ("selected item index found at %s with data: %s" % (index.row(), index.data()))

    def getPath(self,title:str):
        tempstr =  QFileDialog.getExistingDirectory(None, 
                                                      title, 
                                                       QtCore.QDir.rootPath(), 
                                                       QFileDialog.ShowDirsOnly)
        return tempstr
        

    def getSavePath(self)->str:
        filepath, _ =QFileDialog.getSaveFileName(filter="Image (*.png);;Image (*.jpg)")
        return filepath
      
    def showMessageBox(self,text:str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok) 
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()


    #On Browse Button Clicked
    def OnBrowseBtnClicked(self ):
             if(self.folderChoosen == False):
                self.groupBtn.setEnabled(True)
                self.folderChoosen = True


    def OnAnnotateBtnClicked(self):
        if self.selectedImage != "":
            self.annotateBtn.setEnabled(False)
            self.openImageEditWindow(self.selectedImage)
           

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
        outputPath=".\\Annotations\\"+outputImage
        i=1
        while(os.path.exists(outputPath)==True):#if exist add number to name
            outputImage=imageName+"_annotated_"+str(i)+".png"
            outputPath=".\\Annotations\\"+outputImage
            i+=1

        handDrawMode = False # true if hand drawing mode is on
        rectangleMode = True # if True, draw rectangle.
        circleMode = False   # if True, draw circle.
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
                    inputImage=cv2.addWeighted(annotationLayer,1,dummyImage,1,0) #Smth is inherently wrong. I can't pinpoint it though.
                        


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
               self.saveAnnotationSignal.emit(outputPath)
               #cv2.imwrite("./cat.png",inputImage)
            elif k == ord('c'):#Clears with dummy image
               inputImage=dummyImage.copy()
               annotationLayer = np.zeros((inputImage.shape[0],inputImage.shape[1],4), np.uint8)
            elif k == 27:#ESC
               break
        self.annotateBtn.setEnabled(True)
        cv2.destroyAllWindows()   

        

          






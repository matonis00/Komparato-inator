from ast import Str
from dataclasses import dataclass
import math
from pickle import TRUE
    
import numpy as np
import os
import cv2 
@dataclass
class UserInterface():
    __Window: bool = True #There shuld be a window object 


    #def __init__():
       # app=q


    def show():
        pass
    

    def openImageEditWindow(self,imagePath:str):
        if os.path.exists(imagePath)==False:
            return
            
        inputImage = cv2.imread(imagePath)
        tempimageName=os.path.basename(imagePath)
        imageName= tempimageName[ :tempimageName.index(".")]
        annotationLayer = np.zeros((inputImage.shape[0],inputImage.shape[1],4), np.uint8)
        dummyImage=inputImage.copy()

        outputImage=imageName+"_annotated.jpg"
        outputPath="./Annotations/"+outputImage
        i=1
        while(os.path.exists(outputPath)==True):#if exist add number to name
            outputImage=imageName+"_annotated_"+str(i)+".jpg"
            outputPath="./Annotations/"+outputImage
            i+=1

       
        handDrawMode = False # true if hand drawing mode is on
        RectangleMode = True # if True, draw rectangle.
        CircleMode = False # if True, draw circle.
        isDrawing = False# true if mouse is pressed
        ix,iy =-1,-1
        # mouse callback function
        # C - Clear
        # D - Hand draw
        # R - Rectangle
        # E - Circle
        # S - Save
        # ESC - exit

        def draw(event,x,y,flags,param):
            global ix,iy
            global isDrawing# true if mouse is pressed

            if event == cv2.EVENT_LBUTTONDOWN:
                isDrawing = True
                ix,iy = x,y
            elif event == cv2.EVENT_MOUSEMOVE and handDrawMode == True:
                if isDrawing == True:
                    cv2.line(annotationLayer,(ix,iy),(x,y),(0,255,0,255),2)
                    cv2.line(inputImage,(ix,iy),(x,y),(0,255,0,),2)
                    ix,iy = x,y

            elif event == cv2.EVENT_LBUTTONUP:
                isDrawing = False
                if RectangleMode == True:
                    cv2.rectangle(annotationLayer,(ix,iy),(x,y),(0,255,0,255),2)
                    cv2.rectangle(inputImage,(ix,iy),(x,y),(0,255,0),2)
                elif CircleMode == True:
                    sx=int((ix+x)/2)
                    sy=int((iy+y)/2)
                    truR=int(math.sqrt(math.pow(ix-x,2)+math.pow(iy-y,2))/2)
                    cv2.circle(annotationLayer,(sx,sy),truR,(0,0,255,255),2)
                    cv2.circle(inputImage,(sx,sy),truR,(0,0,255,255),2)

        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw)
        while(1):
            cv2.imshow('image',inputImage)
            #cv2.imshow('adnotation',img2)
            k = cv2.waitKey(1)
            if k == ord('r'):#Switch to draw rectangle
               RectangleMode = True
               CircleMode= False
               handDrawMode = False
            elif k == ord('e'):#Switch to draw circle
               RectangleMode = False
               CircleMode= True
               handDrawMode = False
            elif k == ord('d'):#Switch to hand draw
               RectangleMode = False
               CircleMode= False
               handDrawMode=True
            elif k == ord('s'):#saves edits in annotation
               cv2.imwrite(outputPath,annotationLayer)
               cv2.imwrite("./cat.png",inputImage)
            elif k == ord('c'):#Clears with dummy image
               inputImage=dummyImage.copy()
               annotationLayer = np.zeros((inputImage.shape[0],inputImage.shape[1],4), np.uint8)
            elif k == 27:#ESC
               break
            
        cv2.destroyAllWindows()   

        

          






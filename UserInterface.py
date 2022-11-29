from dataclasses import dataclass
import math
    
import numpy as np
import cv2 
@dataclass
class UserInterface():
    __Window: bool = True #There shuld be a window object 


    #def __init__():
       # app=q


    def show():
        pass

img = cv2.imread("nowy.jpg")
img2 = np.zeros((img.shape[0],img.shape[1],4), np.uint8)
temp=img;
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle.
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
  global ix,iy,drawing,mode

  if event == cv2.EVENT_LBUTTONDOWN:
      drawing = True
      ix,iy = x,y

  #elif event == cv2.EVENT_MOUSEMOVE:
  #  if drawing == True:
  #      if mode == True:
  #          cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),3)
  #          a=x
  #          b=y
  #          if a != x | b != y:
  #               cv2.rectangle(img,(ix,iy),(x,y),(0,0,0),-1)
  #      else:
  #          cv2.circle(img,(x,y),5,(0,0,255),-1)
  elif event == cv2.EVENT_LBUTTONUP:
    drawing = False
    if mode == True:
        cv2.rectangle(img2,(ix,iy),(x,y),(0,255,0,255),2)
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),2)

    else:
        sx=int((ix+x)/2)
        sy=int((iy+y)/2)
        truR=int(math.sqrt(math.pow(ix-x,2)+math.pow(iy-y,2))/2)
        cv2.circle(img2,(sx,sy),truR,(0,0,255,255),2)
        cv2.circle(img,(sx,sy),truR,(0,0,255,255),2)


cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
 cv2.imshow('image',img)
 #cv2.imshow('adnotation',img2)
 k = cv2.waitKey(1)
 print(k)
 if k == ord('m'):
    mode = not mode
 elif k == ord('s'):
    cv2.imwrite("./transparent_img.png",img2)
    cv2.imwrite("./cat.png",img)
 elif k == 27:
    break

cv2.destroyAllWindows()   






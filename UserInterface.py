from dataclasses import dataclass
    
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
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),2)

    else:
        cv2.circle(img,(x,y),5,(0,0,255),-1)

#img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
 cv2.imshow('image',img)
 k = cv2.waitKey(1) & 0xFF
 if k == ord('m'):
    mode = not mode
 elif k == 27:
    break

cv2.destroyAllWindows()   






from dataclasses import dataclass
from IO import IO
from UserInterface import UserInterface
from ImageHandler import ImageHandler
import numpy as np
import cv2 

class Session():

    def __init__(self):
        self.__isPremium:bool
        self.userInterface:UserInterface = UserInterface()
        self.handler:ImageHandler = ImageHandler()
        self.InOut:IO=IO()


    def __validateKey(self,key) -> bool:
        pass


    def getUI(self)->UserInterface:
        return self.userInterface

imagePath="nowy.jpg"
sesja = Session()
sesja.getUI().openImageEditWindow(imagePath)

from dataclasses import dataclass
from UserInterface import UserInterface
from ImageHandler import ImageHandler


class Session():

    def _innit__(self):

         __isPremium:bool
         userInterface:UserInterface = UserInterface()
         handler:ImageHandler = ImageHandler()


    def __validateKey(self,key) -> bool:
        pass



sesja = Session()


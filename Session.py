from dataclasses import dataclass
from IO import IO
from UserInterface import UserInterface
from ImageHandler import ImageHandler


class Session():

    def _innit__(self):

         __isPremium:bool
         userInterface:UserInterface = UserInterface()
         handler:ImageHandler = ImageHandler()
         InOut:IO=IO()


    def __validateKey(self,key) -> bool:
        pass



sesja = Session()


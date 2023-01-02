import glob
import os


class IO():
    def __innit__():
        pass

    def loadAnnotation():
        pass

    def saveAnnotation():
        pass

    def loadResult():
        pass

    def saveResult():
        pass

    def readPath(self,sourcePath)->list:
        tempList = list()
        for fileName in glob.iglob(sourcePath + '**/**', recursive=True):
            if os.path.isfile(fileName):
                if fileName.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(fileName)
                    #if fileName not in tempList:
                    tempList.append(fileName)
        return tempList





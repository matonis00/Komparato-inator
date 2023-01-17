from typing import Dict, List

class ResultSet():

    def __init__(self,metricName, resultDict:Dict[str,List[str]]):
        self.content = resultDict
        self.metricName = metricName


    def appendPath(self,key:str,value:str)->bool:
        keyList = self.content.get(key)
        if keyList is None:
             self.content[key] = [value]
        else:
              keyList.append(value)
        return True


    def removePathInKey(self,key:str,path:str)->bool:
        try:
            self.content[key].remove(path)
            return True
        except ValueError:
            return False

    def removePath(self,path:str)->bool:
        try:
            for key, keyList in self.content.items():
                if path in keyList:
                    keyList.remove(path)
                    return True
        except ValueError:
            return False
        return False


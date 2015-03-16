from os.path import getmtime, realpath
from inspect import getfile

class Structure():
    
    def getStructureVersion(self):
        return int(getmtime(realpath(getfile(self.__class__))))

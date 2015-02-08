import pickle
from advanced.dir import getFile
from datetime import time

def readPickle(zdir,pick):
    data = None
    nor = True
    i = 0
    while nor and i < 10:
        i += 1
        try:
            inz = open(getFile(zdir, pick+".pickle"), 'rb')
            data = pickle.load(inz)
            inz.close()
            nor = False
        except EOFError:
            nor = False
        except:
            print("Retry open pickle"+pick)
            time.sleep(1)
    return data

def writePickle(zdir,pick,msg):
    output = open(getFile(zdir, pick+".pickle"), 'wb')
    pickle.dump(msg, output)
    output.close()
    return True
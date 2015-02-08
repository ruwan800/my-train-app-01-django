import os

def getFile(dir1,file):

    if 'OPENSHIFT_REPO_DIR' in os.environ:
        directory = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], dir1)
    else:
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        directory = os.path.join(BASE_DIR, '..', '..', 'data', dir1)
    filedir = os.path.join(directory, file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(filedir):
        open(filedir, 'a').close()
    return(filedir)
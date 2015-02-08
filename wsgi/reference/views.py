from advanced.render import renderJSON
from reference.models import getObject


def view(request,ref):
    obj = getObject(ref)
    try:
        data = obj.getData()
        structure = obj.getStructure()
        return renderJSON(request, {'structure':structure, 'data':data})
    except:
        return renderJSON(request, {'structure':None, 'data':None})

def getData(request,ref):
    obj = getObject(ref)
    try:
        data = obj.getData()
        version = obj.getStructureVersion()
        return renderJSON(request, {'version': version, 'data':data, 'model': obj.__class__.__name__})
    except:
        return renderJSON(request, {'version': None, 'data':None, 'model': None})

def getStructure(request,ref):
    obj = getObject(ref)
    try:
        version = obj.getStructureVersion()
        structure = obj.getStructure()
        return renderJSON(request, {'version': version, 'structure': structure})
    except:
        return renderJSON(request, {'version': None, 'structure': None})
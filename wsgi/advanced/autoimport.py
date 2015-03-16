from importlib import import_module

def importModel(name):
    obj = import_module("{}.models".format(name.lower()))
    return getattr(obj, name)


def importFunction(module,filename,function):
    obj = import_module("{}.{}".format(module.lower(),filename.lower()))
    return getattr(obj, function)
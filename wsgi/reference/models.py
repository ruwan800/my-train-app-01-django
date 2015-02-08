from django.db import models
from importlib import import_module
from advanced.unique import uniqueKey
from advanced.uri import formatText

class ReferenceModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)
    file = models.CharField(max_length=45, unique=True)
    uri = models.CharField(max_length=45, unique=True)
    class Meta:
        db_table = 'reference_model'

    def __unicode__(self):
        return self.name

class Reference(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=40, unique=True)
    uri = models.CharField(max_length=45, null=True, blank=True)
    ref_model = models.ForeignKey(ReferenceModel)
    ref_id = models.IntegerField()
    class Meta:
        db_table = 'reference'

    def __unicode__(self):
        return "{}-{}".format(self.ref_model,self.ref_id)

def getObject(ref):
    """
    Reference.getObject(reference) -> object\n
    Return a required object for the given reference value
    """
    try:
        row = Reference.objects.get(code=ref)
    except:
        return False
    #import external model related to request
    obj = import_module("{}.models".format(row.ref_model.file))
    mod = getattr(obj, row.ref_model.name)
    #retrive row from model
    return mod.objects.get(id=row.ref_id)

def getObjectByName(name):
    try:
        ref = Reference.objects.get(uri=name).code
        return getObject(ref)
    except:
        raise Exception('message',"No item found named '{}'".format(name))

def getModel(ref):
    """
    Reference.getModel(reference) -> model\n
    Return the model of required object for the given reference value
    """
    try:
        row = Reference.objects.get(code=ref)
    except:
        raise Exception('message',"No such reference exists.")
    return row.ref_model
    
def getReference(model, ref_id):
    """
    Reference.createReference(model, ref_id) -> reference\n
    Create and return a reference value if the given model,id combination already
    does not have a reference value\n
    model = model instance\n
    ref_id = id of the object\n
    ref = reference value for the given model, id combination
    """
    Q1 = ReferenceModel.objects.filter(name=model.__name__)
    if Q1:
        Q1 = Q1[0]
    else:
        Q1 = ReferenceModel(name=model.__name__, file=model.__name__.lower(), uri=formatText(model.__name__))
        Q1.save()
    Q2 = Reference.objects.filter(ref_model=Q1, ref_id=ref_id)
    if not Q2:
        obj = import_module("{}.models".format(model.__name__.lower()))
        mod = getattr(obj, model.__name__)
        obj2 = mod.objects.filter(id=ref_id)
        if hasattr(obj2, 'name'):
            Q3 = Reference(code=uniqueKey(), uri=formatText(obj2[0].name), ref_model=Q1, ref_id=ref_id)
        else:
            Q3 = Reference(code=uniqueKey(), ref_model=Q1, ref_id=ref_id)
        Q3.save()
        return Q3.code
    else:
        return Q2[0].code

def getReferenceByObject(obj):
    return getReference(obj.__class__, obj.pk)

def getReferenceByName(name):
    try:
        return Reference.objects.get(uri=name)
    except Reference.DoesNotExist:
        return None

def getURIByObject(obj):
    code = getReference(obj.__class__, obj.pk)
    return Reference.objects.get(code=code).uri

def getReferenceObject(ref):
    return Reference.objects.get(code=ref)

def registerObject(ref):
    getReferenceByObject(ref)

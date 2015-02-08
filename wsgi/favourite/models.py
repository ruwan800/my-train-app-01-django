from django.db import models
from userinfo.models import UserInfo
from reference.models import Reference, getObject, ReferenceModel, getReferenceObject
from advanced.unique import uniqueKey
from advanced.uri import formatText

class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32)
    user = models.ForeignKey(UserInfo)
    history = models.ForeignKey(Reference)
    source = models.ForeignKey(ReferenceModel)
    last_visit = models.DateTimeField(auto_now_add=True)
    frequency = models.IntegerField(default=1)
    favourite = models.BooleanField(default=False)
    class Meta:
        ordering = ['-favourite', '-frequency']
        db_table = 'favourite'

    def __unicode__(self):
        return self

def addToHistory(request, source, ref):
    """
        addToHistory(request, source, ref) -> None
        log history.
        request = request object
        source = source model
        ref = reference object
    """
    try:
        user = UserInfo.objects.get(user=request.user)
    except:
        return
    result = Favourite.objects.filter(user=user, source__name=source.__name__, history__code = ref)
    if result:
        result = result[0]
        result.frequency += 1
        result.save()
    else:
        try:
            Q1 = ReferenceModel.objects.get(name=source.__name__)
        except ReferenceModel.DoesNotExist:
            Q1 = ReferenceModel(name=source.__name__, file=source.__name__.lower(), uri=formatText(source.__name__))
            Q1.save()
        Q = Favourite(code=uniqueKey(), user=user, history=getReferenceObject(ref.code), source=Q1)
        Q.save()

def getFavaurite(request, model):
    """
        getFavaurite(request, model) -> favourites
        returns history elements to given model.
        request = request object
        model = model uri
        favourites = Target receiver list
    """
    user = UserInfo.objects.get(user=request.user)
    result1 = Favourite.objects.filter(user=user, source__uri=model)[:10]
    result = [getObject(x.code).name for x in result1]
    if len(result1) < 10:
        result2 = Favourite.objects.filter(source__uri=model)[:10]
        result += [getObject(x.code).name for x in result2]
    return result[:10]

from django.db import models

UPDATE_STRING = "update_ss"

class Update(models.Model):
    id = models.IntegerField(primary_key=True)
    trace = models.TextField(unique=True, null=False)
    cat1 = models.CharField(max_length=45, null=True, blank=True)
    cat2 = models.CharField(max_length=45, null=True, blank=True)
    value = models.CharField(max_length=45, null=True, blank=True)
    old = models.CharField(max_length=45, null=True, blank=True)
    new = models.CharField(max_length=45, null=True, blank=True)
    time = models.TimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    class Meta:
            db_table = 'log_update'
    def __unicode__(self):
        self.trace

class Conflict(models.Model):
    id = models.IntegerField(primary_key=True)
    trace = models.TextField(unique=True, null=False)
    cat = models.CharField(max_length=45, null=True, blank=True)
    value = models.CharField(max_length=45, null=True, blank=True)
    msg = models.TextField(max_length=45, null=True, blank=True)
    time = models.TimeField(auto_now=True)
    reviewed = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    class Meta:
            db_table = 'log_conflict'
    def __unicode__(self):
        self.trace
class Insert(models.Model):
    id = models.IntegerField(primary_key=True)
    trace = models.TextField(unique=True, null=False)
    cat = models.CharField(max_length=45, null=True, blank=True)
    value = models.CharField(max_length=45, null=True, blank=True)
    msg = models.TextField(max_length=45, null=True, blank=True)
    time = models.TimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    class Meta:
            db_table = 'log_insert'
    def __unicode__(self):
        self.trace
class Delete(models.Model):
    id = models.IntegerField(primary_key=True)
    trace = models.TextField(unique=True, null=False)
    cat = models.CharField(max_length=45, null=True, blank=True)
    value = models.CharField(max_length=45, null=True, blank=True)
    msg = models.TextField(max_length=45, null=True, blank=True)
    time = models.TimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    class Meta:
            db_table = 'log_delete'
    def __unicode__(self):
        self.trace


def addUpdate(cat1, cat2, value, old, new):
    """ mention updated item in update list. """
    trace = "{} - {} - {} - {} - {}".format(cat1, cat2, value, old, new)
    Q = Update.objects.filter(trace=trace)
    if not Q:
        Q1 = Update(cat1=cat1, cat2=cat2, value=value, old=old, new=new, trace=trace)
        Q1.save()

def addConflict(cat, value, msg):
    """ mention items with conflicts in conflict list. """
    trace = "{} - {} - {}".format(cat, value, msg)
    Q = Conflict.objects.filter(trace=trace)
    if Q:
        Q[0].resolved = False
        Q[0].save()
    else:
        Q1 = Conflict(cat=cat, value=value, msg=msg, trace=trace)
        Q1.save()

def addInsert(cat, value, msg):
    """ mention inserted items. """
    trace = "{} - {} - {}".format(cat, value, msg)
    Q = Insert.objects.filter(trace=trace)
    if not Q:
        Q1 = Insert(cat=cat, value=value, msg=msg, trace=trace)
        Q1.save()

def addDelete(cat, value, msg):
    """ mention deleted items. """
    trace = "{} - {} - {}".format(cat, value, msg)
    Q = Delete.objects.filter(trace=trace)
    if not Q:
        Q1 = Delete(cat=cat, value=value, msg=msg, trace=trace)
        Q1.save()




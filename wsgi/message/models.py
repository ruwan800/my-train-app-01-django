from django.db import models
from notification.models import saveTarget
from advanced.user import getUser, getUserName
from advanced.unique import uniqueKey
from favourite.models import addToHistory
from userinfo.models import UserInfo
from group.models import Group
from station.models import Station, getStation
from train.models import Train, getTrain
from advanced.cloud import send
from group.groupset import StationUsers
from numpy.ctypeslib import ctypes


class Thread(models.Model):
    STATUS_CHOICES = ((0, 'station'), (1, 'train'))
    id = models.AutoField(primary_key=True)
    c_type = models.IntegerField(choices=STATUS_CHOICES)
    ref = models.IntegerField()

    class Meta:
        db_table = 'mta_user_thread'

    def __unicode__(self):
        return "{}-{}".format(self.c_type, self.ref)

    def get_reference(self):
        if self.c_type == self.STATUS_CHOICES[0][0]:
            return Station.objects.get(pk=self.ref)
        else:
            return Train.objects.get(pk=self.ref)

    def get_c_type(self):
        if self.c_type == Thread.STATUS_CHOICES[0][0]:
            return Thread.STATUS_CHOICES[0][1]
        else:
            return Thread.STATUS_CHOICES[1][1]



class Message(models.Model):
    id = models.AutoField(primary_key=True)
    thread = models.ForeignKey(Thread)
    sender = models.ForeignKey(UserInfo)
    dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    star = models.IntegerField(default=False)

    class Meta:
        ordering = ['dt']
        db_table = 'mta_user_message'

    def __unicode__(self):
        return self.text


def get_thread(thread_id):
    return Thread.objects.get(pk=thread_id)


class StationMessage(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserInfo)
    receiver = models.ForeignKey(Station)
    dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    received = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)

    class Meta:
        ordering = ['dt']
        db_table = 'mta_station_message'

    def __unicode__(self):
        return self.text


class TrainMessage(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserInfo)
    receiver = models.ForeignKey(Train)
    dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    received = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)

    class Meta:
        ordering = ['dt']
        db_table = 'mta_train_message'

    def __unicode__(self):
        return self.text


class PublicMessage(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserInfo)
    dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    received = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)

    class Meta:
        ordering = ['dt']
        db_table = 'mta_public_message'

    def __unicode__(self):
        return self.text


def saveMessage(request, message, m_type, target):
    """
        saveMessage(msg, target, m_type, request) -> None
        save new comment.
        target = Target receiver
        m_type = Target type
        request = request object
        message = Message text
    """
    result = None
    if m_type== "USER" :
        sender = getUser(request.user)
        receiver=UserInfo.objects.get(pk=target)
        sendUserMessage(sender, receiver, message)
        Q = Message(sender=getUser(request.user), receiver=getUserName(target), text=message)
    elif  m_type== "STATION" :
        sender = getUser(request.user)
        receiver=getStation(target)
        sendStationMessage(sender, receiver, message)
        Q = StationMessage(sender=sender, receiver=receiver, text=message)
    elif  m_type== "TRAIN" :
        sender = getUser(request.user)
        receiver=getTrain(target)
        sendTrainMessage(sender, receiver, message)
        Q = TrainMessage(sender=getUser(request.user), receiver=getTrain(target), text=message)
    elif  m_type== "PUBLIC" :
        sender = getUser(request.user)
        sendPublicMessage(sender, message)
        Q = PublicMessage(sender=getUser(request.user), text=message)
    else:
        return;
    Q.save()
    return result
    #addToHistory(request, Message, target)
    #Q1 = Group.objects.get(name='singleItem')
    
    #saveTarget(Message,Q.pk,[[getReferenceByObject(Q1),target]])

def getThread(c_type, cid):
    """
        getThread(request, target) -> messages
        Views a conversation.
        request = request object
        target = Target user
        messages = List of messages sorted by date
    """
    type_int = get_thread_type_id(c_type)
    q0 = Thread.objects.filter(c_type=type_int, ref=cid)
    if not q0:
        return None
    return q0[0]


def get_thread_type_id(c_type):
    if c_type == Thread.STATUS_CHOICES[0][1]:
        return Thread.STATUS_CHOICES[0][0]
    else:
        return Thread.STATUS_CHOICES[1][0]

def sendUserMessage(sender, receiver, message):
    
    recipients  = StationUsers(receiver)
    #if(sender in recipients):
    #    recipients.remove(sender)
    
    data = {}
    data['Type'] = "MESSAGE"
    data['Message'] = message
    data['Sender'] = sender.name
    data['Target'] = receiver.name
    data['MessageType'] = "USER"
    data['SenderReference'] = sender.id
    data['TargetReference'] = receiver.id
    
    return send(recipients, data)

def sendStationMessage(sender, receiver, message):
    
    recipients  = StationUsers(receiver)
    #if(sender in recipients):
    #    recipients.remove(sender)
    
    data = {}
    data['Type'] = "MESSAGE"
    data['Message'] = message
    data['Sender'] = sender.name
    data['Target'] = receiver.name
    data['MessageType'] = "STATION"
    data['SenderReference'] = sender.id
    data['TargetReference'] = receiver.name
    
    return send(recipients, data)

def sendTrainMessage(sender, receiver, message):
    
    recipients  = StationUsers(receiver)
    #if(sender in recipients):
    #    recipients.remove(sender)
    
    data = {}
    data['Type'] = "MESSAGE"
    data['Message'] = message
    data['Sender'] = sender.name
    data['Target'] = receiver.name
    data['MessageType'] = "TRAIN"
    data['SenderReference'] = sender.id
    data['TargetReference'] = receiver.number
    
    return send(recipients, data)

def sendPublicMessage(sender, message):
    
    #recipients  = StationUsers(receiver)
    recipients  = UserInfo.objects.all()
    #if(sender in recipients):
    #    recipients.remove(sender)
    
    data = {}
    data['Type'] = "MESSAGE"
    data['Message'] = message
    data['Sender'] = sender.name
    data['MessageType'] = "PUBLIC"
    data['SenderReference'] = sender.id
    
    return send(recipients, data)
    
    
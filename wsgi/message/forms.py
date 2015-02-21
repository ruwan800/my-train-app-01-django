from django.forms import ModelForm
from message.models import Message
#from django.forms.widgets import Textarea

class MessageForm(ModelForm):
    class Meta:
        model = Message
        #fields = ['receiver', 'text']
        #widgets={'receiver': Textarea()}
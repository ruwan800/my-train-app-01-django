from django.forms import ModelForm
from message.models import UserMessage
from django.forms.widgets import Textarea

class MessageForm(ModelForm):
    class Meta:
        model = UserMessage
        fields = ['receiver', 'text']
        widgets={'receiver': Textarea()}
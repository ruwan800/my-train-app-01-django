from django.forms import ModelForm
from comment.models import Comment
from django.forms.widgets import Textarea

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['ref', 'text']
        widgets={'ref': Textarea()}
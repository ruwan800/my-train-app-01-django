from django.forms import ModelForm
from station.models import Station


class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['line', 'name']
        #widgets={'target': HiddenInput()}
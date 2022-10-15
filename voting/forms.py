from django import forms
from django.forms import modelformset_factory

from .models import Poll, Option


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Poll
        fields = ['question']


class ChoiceForm(forms.Form):
    choice = forms.CharField(label='choice', max_length=1000)
    

OptionFormSet = modelformset_factory(
    Option, fields=("text", ), min_num=2, max_num=30,
)
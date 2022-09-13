from django import forms

from .models import Poll


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Poll
        fields = ['question']


class ChoiceForm(forms.Form):
    choice = forms.CharField(label='choice', max_length=1000)
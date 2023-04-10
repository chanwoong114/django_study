from django import forms
from .models import Chatting

class ChattingForm(forms.ModelForm):
    class Meta:
        model = Chatting
        fields = '__all__'
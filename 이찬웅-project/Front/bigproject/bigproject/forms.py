from django import forms
from signup.models import User
        
class PostForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['upload']

from django import forms
from .models import Question, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        labels = {
            'issue_a': 'RED_TEAM',
            'issue_b': 'BLUE_TEAM',
            }

class CommentForm(forms.ModelForm):
    pick = forms.CharField(
        widget = forms.Select(
            choices=[
                (True, 'RED_TEAM'),
                (False, 'BLUE_TEAM')
            ]
        )
    )

    class Meta:
        model = Comment
        exclude = ['question']
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget = forms.TextInput(
            attrs = {
                'class': 'my-title',
                'placeholder': 'ex) 세 얼간이',
            }
        )
    )

    director = forms.CharField(
        label = '감독',
        widget = forms.TextInput(
            attrs = {
                'class': 'my-director',
                'placeholder': 'ex) 라지쿠마르 히라니' ,
            }
        )
    )

    comment = forms.CharField(
        label = '댓글',
        widget = forms.Textarea(
            attrs = {
                'class': 'my-comment',
                'placeholder': 'ex) 나 얼간이 아니다',
                'row': 3,
                'col': 40,
            }
        ),
        error_messages = {
            'required': 'Please enter your content'
        }
    )

    class Meta:
        model = Movie
        fields = '__all__'
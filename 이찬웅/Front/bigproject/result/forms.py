from django import forms
from result.models import Result

class ResultForm(forms.ModelForm): # 모델 폼을 상속받은 QuestionForm 클래스
  class Meta: # 내부 Meta 클래스
    model = Result
    fields = ['file']
    # labels 코드 추가하기
    labels = {
      'file' : '첨부파일',
    }
    
from django import forms
from home.models import Question, Answer, Sheet

class QuestionForm(forms.ModelForm): # 모델 폼을 상속받은 QuestionForm 클래스
  class Meta: # 내부 Meta 클래스
    model = Question
    fields = ['subject', 'content', 'imgfile']
    # labels 코드 추가하기
    labels = {
      'subject' : '제목',
      'content' : '내용',
      'imgfile' : '첨부파일',
    }
    
class AnswerForm(forms.ModelForm): # 모델 폼을 상속받은 QuestionForm 클래스
  class Meta: # 내부 Meta 클래스
    model = Answer
    fields = ['content']
    # labels 코드 추가하기
    labels = {
      'content' : '내용',
    }
    
class SheetForm(forms.ModelForm): # 모델 폼을 상속받은 QuestionForm 클래스
  class Meta: # 내부 Meta 클래스
    model = Sheet
    fields = ['imgfile']
    # labels 코드 추가하기
    labels = {
      'imgfile' : '첨부파일',
    }
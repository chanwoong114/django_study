from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def hello(request):
    return render(request, 'home/hello.html')

def question_list(request):
  questions = Question.objects.order_by('-create_date') # Question 모델 데이터를 작성일시의 역순(-)으로 정렬한다.
  # Paging 기능 구현하기
  page = request.GET.get('page', '1') # GET 방식 요청 URL에서 page값을 가져올 때 사용(?page=1). page 파라미터가 없는 URL을 위해 기본값으로 1을 지정한 것
  paginator = Paginator(questions, 5) # Paginator 클래스는 questions를 페이징 객체 paginator로 변환. 페이지당 5개씩 보여주기
  page_obj = paginator.get_page(page) # page_obj 객체에는 여러 속성이 존재
  context = { 'questions_list' : page_obj } # page_obj를 question_list에 저장한다.
  return render(request, 'home/question_list.html', context)

def question_detail(request, question_id):
  # question = Question.objects.get(id=question_id) # urls에 mapping된 question_id와 같은 것
  question = get_object_or_404(Question, pk=question_id) # 404페이지 출력하기
  context = { 'a_question' : question} # 위의 question를 context 변수인 a_question에 저장한다.
  return render(request, 'home/question_detail.html', context)

 
# def answer_create(request, question_id):
#   if request.user.is_anonymous:
#     return redirect('users:login')
#   else:
#     a_question = get_object_or_404(Question, pk=question_id) # 어떤 question 글에 달린 answer?
#     a_content = request.POST.get('content') # 뒤에 content는 html>name이랑 같다
#     if a_content:
#       Answer.objects.create(question = a_question, content = a_content, user = request.user) # models.py = views.py
#       return redirect('home:question_detail', question_id=a_question.id)
#     else:
#       messages.warning(request, "답변을 입력해주세요.")
#       return redirect('home:question_detail', question_id=a_question.id)

def answer_create(request, question_id):
  if request.user.is_anonymous:
    return redirect('users:login')
  else:
    a_question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
      a_form = AnswerForm(request.POST)
      if a_form.is_valid():
        answer = a_form.save(commit=False) # 폼에 없는 필드인 create_date부분을 자동입력으로 모델을 설정하였기 때문에 a_form.save()라고 작성하여도 오류가 발생하지는 않는다.
        answer.user = request.user
        answer.question = a_question
        answer.save()
        return redirect('home:question_detail', question_id=a_question.id)
      else:
        messages.warning(request, "답변을 입력해주세요.")
        return redirect('home:question_detail', question_id=a_question.id)
    else: # request.method == 'GET'인 경우
      a_form = AnswerForm(request.GET) # QuestionForm 클래스로 생성한 객체 a_form을 사용할 것이다.
    context = {'form' : a_form }
    return render(request, 'home/question_detail.html', context)


def question_create(request):
  if request.user.is_anonymous:
    return redirect('users:login')
  else:
    if request.method == 'POST':
      a_form = QuestionForm(request.POST)
      if a_form.is_valid():
        question = a_form.save(commit=False) # 폼에 없는 필드인 create_date부분을 자동입력으로 모델을 설정하였기 때문에 a_form.save()라고 작성하여도 오류가 발생하지는 않는다.
        question.user = request.user
        question.save()
        files = request.FILES.getlist('imgfile')
        for a in files:
          print(1)
          sheet = Sheet()
          sheet.questions = question
          sheet.imgfile = a
          sheet.save()
        return redirect('home:question_list')
    else: # request.method == 'GET'인 경우
      a_form = QuestionForm() # QuestionForm 클래스로 생성한 객체 a_form을 사용할 것이다.
    context = {'form' : a_form }
    return render(request, 'home/question_form.html', context)
  
def question_edit(request, pk):
  question = Question.objects.get(id=pk)
  if request.method == "POST":
    if(question.user == request.user or request.user.is_staff == True):
      form = QuestionForm(request.POST, instance=question)
      if form.is_valid():
        question = form.save(commit = False)
        question.save()
        if request.FILES:
          print(1)
          sheet = Sheet.objects.filter(questions_id=pk)
          sheet.delete()
          files = request.FILES.getlist('imgfile')
          for a in files:
            sheet = Sheet()
            sheet.questions = question
            sheet.imgfile = a
            sheet.save()
        return redirect('home:question_detail', question_id=question.id)
  else:
    question = Question.objects.get(id=pk)
    if question.user == request.user or request.user.is_staff == True:
      form = QuestionForm(instance=question)
      context = {
          'form': form,
          'edit': '수정하기',
        }
      return render(request, "home/question_form.html", context)
    else:
      return redirect('home:question_detail', question_id=question.id)
    
    
def question_delete(request, pk):
  question = Question.objects.get(id=pk)
  if question.user == request.user or request.user.is_staff == True:
    question.delete()
    return redirect('home:question_list')
  else:
    return redirect('home:question_detail', question_id=question.id)
  
def answer_delete(request, pk):
  answer = Answer.objects.get(id=pk)
  if answer.user == request.user or request.user.is_staff == True:
    answer.delete()
    return redirect('home:question_detail', question_id=answer.question_id)
  else:
    return redirect('home:question_detail', question_id=answer.question_id)
  
  
def search(request):
  post = Question.objects.all().order_by('-id')
  search_type = request.GET.get('search_type', '')
  post = post.order_by('-create_date')
  q = request.GET.get('q', "") 

  if q:
    if len(q) > 1 :
      if search_type == 'all':
        post_list = post.filter( Q(subject__icontains=q) | Q(content__icontains=q) | Q(user__username__icontains=q))
      elif search_type == 'subject_content':
        post_list = post.filter( Q(subject__icontains=q) | Q(content__icontains=q))
      elif search_type == 'subject':
        post_list = post.filter(subject__icontains=q)    
      elif search_type == 'content':
        post_list = post.filter(content__icontains=q)    
      elif search_type == 'writer':
        post_list = post.filter(user__username__icontains=q)
      post_list = post_list.order_by('-create_date')
      page = request.GET.get('page', '1')
      paginator = Paginator(post_list, 5) # Paginator 클래스는 questions를 페이징 객체 paginator로 변환. 페이지당 5개씩 보여주기
      page_obj = paginator.get_page(page) # page_obj 객체에는 여러 속성이 존재
      context = { 'post' : page_obj, 'q' : q, 'search_type' : search_type }
      return render(request, 'home/question_list.html', context)
    
    else:
      messages.error(request, '검색어는 2글자 이상 입력해주세요.')
      return redirect('home:question_list')
    
  else:
    messages.warning(request, "검색어를 입력해주세요.")
    return redirect('home:question_list')
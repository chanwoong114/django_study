from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'eithers/index.html', context)

def detail(request, pk):
    question = Question.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = question.comment_set.all()
    context = {'question': question,
               'comment_form': comment_form,
               'comments': comments}
    return render(request, 'eithers/detail.html', context)

def create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eithers:index')
    else:
        form = QuestionForm()
    
    context = {'form': form}
    return render(request, 'eithers/create.html', context)

def comment(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.question = question
            comment.save()
    return redirect('eithers:detail', question_pk)

def random(request):
    random_question = Question.objects.order_by('?')[0]

    return redirect('eithers:detail', random_question.id)

def update(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('eithers:detail', question.pk)
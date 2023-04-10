from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from home.models import *
from .forms import PostForm
from signup.models import *
from result.models import *


def main(request):
  return render(request, 'main.html')

def index(request):
    return render(request, 'index.html')
  

def upload1(request):
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES) # NOTE: 인자 순서주의 POST, FILES
		#modelform = PostForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.music = request.FILES.get('music',None)
			form.save()
			return redirect('upload')
	else:
		form = PostForm()
	return render(request, 'upload.html',{
		'form': form,
	})

def musicfile(request):
	if request.method == 'GET':
		modelform = PostForm()
		return render(request, 'upload.html', {'modelform': modelform})
	elif request.method == 'POST':
		modelform = PostForm(request.POST)
		if modelform.is_valid():
			post = modelform.save(commit=False)
			post.music = request.FILES.get('music',None)
			post.save()
			return redirect('upload')

def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file  = request.FILES.get('file')
        
        
        
        

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def hello(request):
    menu = ['햄버거', '피자', '치킨']

    return render(request, 'articles/hello.html', {'menu':menu})

def index(request):
    return render(request, 'articles/index.html')

def hello2(request, name):
    print(name)
    context = {
        'name': name,
    }
    return render(request, 'articles/hello2.html', context)
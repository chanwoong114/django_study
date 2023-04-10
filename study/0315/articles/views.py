from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'articles/index.html')

def hello(request):
    m = 'hello'
    context = {
        'message': m
    }

    return render(request, 'articles/hello.html', context)

def hello2(request, name, age):
    context = {
        'name': name,
        'age': age
    }

    return render(request, 'articles/hello2.html', context)
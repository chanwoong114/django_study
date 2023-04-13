from django.shortcuts import render

# Create your views here.

def newhello(request):
    return render(request, 'movies/new_hello.html')

def index(request):
    return render(request, 'movies/index.html')
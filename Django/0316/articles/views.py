from django.shortcuts import render

from articles.models import Article

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')

def throw(request):
    return render(request, 'articles/throw.html')

def catch(request):
    message = request.GET.get('message')
    title = Article.objects.get(id=1)
    context = {
        'message': message,
        'title': title,
    }
    return render(request, 'articles/catch.html', context)
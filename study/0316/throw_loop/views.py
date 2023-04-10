import random
from django.shortcuts import render

# Create your views here.
def first(request):
    message = 'nothing'
    if request.GET.get('message'):
        message = request.GET.get('message')
    context = {
        'message': message
    }
    return render(request, 'throw_loop/first.html', context)

def second(request):
    message = request.GET.get('message')
    context = {
        'message': message
    }
    return render(request, 'throw_loop/second.html', context)

def third(request):
    message = []
    message.append(request.GET.get('message1'))
    message.append(request.GET.get('message2'))

    message = message[random.choice([0, 1])]

    context = {
        'message': message
    }   
    return render(request, 'throw_loop/third.html', context)
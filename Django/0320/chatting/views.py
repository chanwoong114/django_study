from django.shortcuts import redirect, render

from chatting.forms import ChattingForm
from .models import Chatting
# Create your views here.
def index(request):
    chatting = Chatting.objects.all()
    context = {
        'chattings': chatting
    }
    return render(request, 'chatting/index.html', context)

def detail(request, pk):
    chatting = Chatting.objects.get(pk=pk)
    context = {
        'chatting': chatting
    }
    return render(request, 'chatting/detail.html', context)

def create(request):
    if request.method == 'POST':
        form = ChattingForm(request.POST)
        if form.is_valid:
            chatting = form.save()
            return redirect('chatting:index')
    else:
        form = ChattingForm()

    context = {'form' : form}
    return render(request, 'chatting/create.html', context)
    
def update(request, pk):
    chatting = Chatting.objects.get(pk=pk)
    if request.method == 'POST':
        chatting.user = request.POST.get('user')
        chatting.content = request.POST.get('content')
        chatting.save()
        return redirect('chatting:detail', chatting.id)
    else:
        context = {'chatting': chatting}
        return render(request, 'chatting/update.html', context)
    
def delete(request, pk):
    chatting = Chatting.objects.get(pk=pk)
    if request.method == 'POST':
        chatting.delete()
        return redirect('chatting:index')
    else:
        redirect('articles:detail', chatting.pk)
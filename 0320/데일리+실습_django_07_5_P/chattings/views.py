from django.shortcuts import redirect, render, get_object_or_404
from .models import Chat
from .forms import ChatForm
from django.views.decorators.http import require_POST, require_http_methods, require_safe

# Create your views here.

@require_safe
def index(request):
    chattings = Chat.objects.all()
    context = {
        'chattings':chattings
    }
    return render(request,'chattings/index.html',context)

@require_http_methods(["GET","POST"])
def create(request):
    if request.method == 'POST':
        form = ChatForm(request.POST,request.FILES)
        if form.is_valid:
            chatting = form.save()
            return redirect('chattings:detail',chatting.pk)
    else:
        form = ChatForm()
    context={
        'form':form
    }
    return render(request,'chattings/create.html',context)

@require_safe
def detail(request,pk):
    chatting = get_object_or_404(Chat,pk=pk)
    context = {
        'chatting':chatting,
    }
    return render(request,'chattings/detail.html',context)

@require_POST
def delete(request,pk):
    chatting = get_object_or_404(Chat,pk=pk)
    chatting.delete()
    return redirect("chattings:index")

@require_http_methods(["GET","POST"])
def update(request,pk):
    chatting = get_object_or_404(Chat,pk=pk)
    if request.method == "POST":
        form = ChatForm(request.POST, request.FILES, instance = chatting)
        if form.is_valid:
            chatting = form.save()
            return redirect("chattings:detail",chatting.pk)
    else:
        form = ChatForm(instance=chatting)
    context = {
        'chatting':chatting,
        'form':form,
    }
    return render(request,"chattings/update.html",context)


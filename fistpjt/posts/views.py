from django.shortcuts import redirect, render
from posts.forms import postForm
from posts.models import Post

# Create your views here.
def index(request):
    post = Post.objects.all()
    context = {'posts': post}
    return render(request, 'posts/index.html', context)

def create(request):
    if request.method == 'POST':
        form = postForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')

    form = postForm()
    context = {'form': form}
    return render(request, 'posts/create.html', context)

def delete(requestm, pk):
    Post.objects.get(pk=pk).delete()
    return redirect('posts:index')

def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = postForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    
    form = postForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'posts/update.html', context)
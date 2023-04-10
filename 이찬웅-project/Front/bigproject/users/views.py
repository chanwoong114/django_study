from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages, auth


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'users/login1.html', {'error_message': error_message})

    else:
        return render(request, 'users/login1.html')


def mypage(request):
    if request.user.is_anonymous:
        return redirect("users:login")
    else:
        return render(request, 'users/profile.html')


# def update(request):
#     user_change_form = UserChangeForm(instance=request.user)
#     return render(request, 'users/profile.html', {'user_change_form': user_change_form})


def update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(
            request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('users:mypage')

    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        return render(request, 'users/update.html',
                      {'user_change_form': user_change_form})


def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('main')
    return render(request, 'users/delete.html')


# @login_required
# def password(request):
#     if request.method == 'POST':
#         password_change_form = PasswordChangeForm(request.user, request.POST)

#         if password_change_form.is_valid():
#             # 추가된 부분
#             user = password_change_form.save()
#             update_session_auth_hash(request, user)
#             # 끝
#             return redirect('main')

#     else:
#         password_change_form = PasswordChangeForm(request.user)
#     return render(request, 'users/password.html', {
#         'password_change_form': password_change_form
#     })

@login_required
def password(request):
  if request.method == "POST":
    user = request.user
    origin_password = request.POST["origin_password"]
    if check_password(origin_password, user.password):
      new_password = request.POST["new_password"]
      confirm_password = request.POST["confirm_password"]
      if new_password == confirm_password:
        user.set_password(new_password)
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('users:mypage')
      else:
        messages.error(request, 'Password not same')
    else:
      messages.error(request, 'Password not correct')
    return render(request, 'change_password.html')
  else:
    return render(request, 'change_password.html')

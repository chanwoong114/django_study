from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password1'] and request.POST['password2'] and request.POST['email']:
            if not User.objects.filter(username=request.POST['username']):
                if request.POST['password1'] == request.POST['password2']:
                    username = request.POST['username']
                    password = request.POST['password1']
                    email = request.POST['email']

                    # 사용자 생성
                    user = User.objects.create_user(username, email, password)

                    # 사용자 인증
                    user = authenticate(username=username, password=password)

                    # 세션 생성
                    login(request, user)
                    print('success')
                    # 페이지 이동
                    return redirect('main')
                else:
                    messages.warning(request, "비밀번호가 일치하지 않습니다.")
                    return render(request, 'signup/signup1.html')
            else:
                messages.warning(request, "이미 사용중인 아이디 입니다.")
                return render(request, 'signup/signup1.html')
        else:
            messages.warning(request, "필수 항목을 입력해주세요.")
            return render(request, 'signup/signup1.html')
    else: 
        return render(request, 'signup/signup1.html')

def block_mypage(request):
    cur_user = request.user

    if cur_user.is_authenticated:
        user = User.objects.get(request=user)
        return render(request, 'profile.html', {'user':user})
    else:
        return redirect('login1.html')
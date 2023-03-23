from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *
from .models import *


app_name = 'users'
urlpatterns = [
    path('login/', signup, name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', mypage, name='mypage'),
    path('update/', update, name='update'),
    path('delete', delete, name='delete'),
    # path('password/', password, name='password'),
    path('update/', update, name='update'),
    path('password/', password, name='change_password')
]

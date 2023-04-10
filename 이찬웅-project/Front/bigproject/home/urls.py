from django.urls import path
from .views import *
from . import views

app_name = "home" # 앱 이름 설정
urlpatterns = [
    path('go_hello/', hello, name="hello"),
    path('', question_list, name="question_list"),
    path('<int:question_id>/', question_detail, name="question_detail"),
    path('answer/create/<int:question_id>/', answer_create, name="answer_create"),
    path('question_create/', question_create, name="question_create"),
    path('<int:pk>/edit/', question_edit, name='question_edit'),
    path('<int:pk>/delete/', question_delete, name='question_delete'),
    path('<int:pk>/answer/delete/', answer_delete, name='answer_delete'),
    path('search/', search, name="search"),
]
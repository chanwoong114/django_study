from django.urls import path
from .views import *
from . import views

app_name = "result" # 앱 이름 설정
urlpatterns = [
    path('result_create', result_create, name="result"),
    path('', result_list, name="result_list"),
    path('download/', file_download, name='file_download'),
    path('<int:result_id>', result_detail, name="result_detail"),
]
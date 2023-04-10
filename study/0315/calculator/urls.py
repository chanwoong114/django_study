from django.urls import path
from . import views

app_name = 'calculator'
urlpatterns = [
    path('', views.input, name = 'input'),
    path('result/', views.output, name = 'output'),
    path('calculator/<int:no1>/<int:no2>/', views.cal, name = 'cal')
]

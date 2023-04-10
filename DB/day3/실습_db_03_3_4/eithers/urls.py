from django.urls import path
from . import views

app_name = 'eithers'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:question_pk>/comment/', views.comment, name='comment'),
    path('random/', views.random, name='random'),
    path('<int:pk>/update/', views.update, name='update'),
]

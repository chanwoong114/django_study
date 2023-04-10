from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delele/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update')
]

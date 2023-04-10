from django.urls import path
from . import views

app_name = 'eithers'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:question_pk>/', views.detail, name='detail'),
    path('random/', views.random, name='random'),
    path('<int:question_pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:question_pk>/update/', views.update, name='update'),
    path('<int:question_pk>/delete/', views.delete, name='delete'),
    path('<int:question_pk>/delete/<int:comment_pk>/', views.comment_delete, name='comment_delete')
]
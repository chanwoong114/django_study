from django.urls import path, include
from articles import views
app_name = 'articles'
urlpatterns = [
    path('', views.hello, name='hello'),
    path('<name>/', views.hello2),
]
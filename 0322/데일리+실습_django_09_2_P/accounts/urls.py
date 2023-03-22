from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login1, name='login'),
    path('logout/', views.logout1, name='logout')
]
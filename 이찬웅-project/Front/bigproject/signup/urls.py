from django.urls import path
from .views import *

app_name = 'signup'

urlpatterns = [
    path('', signup, name='signup'),
]
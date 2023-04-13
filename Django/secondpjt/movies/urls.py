from django.urls import path, include
from movies import views
import movies


urlpatterns = [
    path('', views.newhello)
]

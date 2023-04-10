from django.urls import path
from . import views

app_name = 'prices'
urlpatterns = [
    path('<thing>/<int:num>/', views.price, name = 'price')
]

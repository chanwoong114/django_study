from django.urls import path
from . import views


urlpatterns = [
    path('musics/', views.music_list),
    path('musics/<int:musics_pk>/', views.music_detail),
]

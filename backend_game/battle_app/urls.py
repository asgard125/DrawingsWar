from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_battle_session', views.battle_session, name='battle_session'),
    path('<str:room_name>/', views.room, name='room'),
]


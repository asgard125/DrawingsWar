"""backend_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, re_path, include
from game_app.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'battleunit', BattleUnitAPIView, basename='battleunit')
router.register(r'user', UserAPIView, basename='user')
router.register(r'playerbattleunit', PlayerBattleUnitAPIView, basename='playerbattleunit')
router.register(r'battlehistory', BattleHistoryAPIView, basename='battlehistory')

urlpatterns = [
    path('battle/', include('battle_app.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls))
]

from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from .serializers import *


class BattleUnitAPIView(generics.ListAPIView):
    queryset = BattleUnit.objects.all()
    serializer_class = BattleUnitSerializer


class BattleUnitAPIView(APIView):
    def get(self, response):
        pass

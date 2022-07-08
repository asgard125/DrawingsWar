from django.shortcuts import render
from rest_framework.response import Response


def index(request):
    return render(request, 'battle_app/index.html')
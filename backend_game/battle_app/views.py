from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.response import Response

from battle_app.models import BattleSession


def index(request):
    return render(request, 'battle_app/index.html')


@login_required
def battle_session(request):
    return Response({'room_code': BattleSession.get_available_room()})


def room(request, room_name):
    return render(request, 'battle_app/room.html', {
        'room_name': room_name
    })
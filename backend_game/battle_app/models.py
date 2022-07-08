from django.db import models
from game_app.models import User
import random
# Create your models here.


class BattleSession(models.Model):
    room_code = models.CharField(max_length=100)
    started = models.BooleanField(default=False)
    players_count = models.IntegerField(default=0)

    @staticmethod
    def get_available_room():
        rooms = BattleSession.objects.all().order_by('-room_code')
        available_rooms = [i for i in rooms if i.players_count < 2]
        if len(available_rooms) == 0:
            if len(rooms) > 0:
                room_code = int(rooms[0].room_code) + 1
            else:
                room_code = 1
            new_room = BattleSession(room_code=room_code)
            new_room.save()
            return str(room_code)
        return str(random.choice(available_rooms).room_code)


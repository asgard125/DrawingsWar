from django.db import models
import random
# Create your models here.


class BattleSession(models.Model):
    room_code = models.CharField(max_length=100)
    player_1_id = models.IntegerField(null=True)
    player_2_id = models.IntegerField(null=True)
    player_1_game_name = models.CharField(max_length=100, blank=True)
    player_2_game_name = models.CharField(max_length=100, blank=True)
    is_started = models.BooleanField(default=False)

    @staticmethod
    def get_available_room():
        rooms = BattleSession.objects.all().order_by('-room_code')
        available_rooms = [i for i in rooms if not i.is_started]
        if len(available_rooms) == 0:
            if len(rooms) > 0:
                room_code = int(rooms[0].room_code) + 1
            else:
                room_code = 1
            new_room = BattleSession(room_code=room_code)
            new_room.save()
            return str(room_code)
        return str(random.choice(available_rooms).room_code)


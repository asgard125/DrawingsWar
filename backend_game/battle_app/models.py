from django.db import models

# Create your models here.


class BattleSession(models.Model):
    room_code = models.CharField(max_length=100)
    player_1_id = models.IntegerField(null=True)
    player_2_id = models.IntegerField(null=True)
    player_1_game_name = models.CharField(max_length=100, blank=True)
    player_2_game_name = models.CharField(max_length=100, blank=True)
    is_started = models.BooleanField(default=False)

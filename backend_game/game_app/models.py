from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    game_name = models.CharField(max_length=30, blank=True, verbose_name='Игровое имя', unique=False)
    rating = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    defeats = models.IntegerField(default=0)
    level_score = models.IntegerField(default=0)
    money = models.IntegerField(default=100)
    deck_size = models.IntegerField(default=3)
    units_in_deck = models.IntegerField(default=0)

    REQUIRED_FIELDS = ('game_name', )


class BattleUnit(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name='Название', unique=True)
    sprite_texture = models.ImageField(verbose_name='Текстура персонажа', blank=True)
    shop_price = models.IntegerField(blank=True, null=True)
    start_level_buy = models.IntegerField(default=1)
    max_level = models.IntegerField(blank=True, null=True)
    start_health_points = models.IntegerField(blank=True, null=True)
    start_shield_level = models.IntegerField(blank=True, null=True)
    start_attack_points = models.IntegerField(blank=True, null=True)
    max_health_points = models.IntegerField(blank=True, null=True)
    max_shield_level = models.IntegerField(blank=True, null=True)
    max_attack_points = models.IntegerField(blank=True, null=True)
    max_move_range = models.IntegerField(blank=True, null=True)
    max_attack_range = models.IntegerField(blank=True, null=True)
    battle_class = models.CharField(max_length=50, blank=True, verbose_name='Класс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонаж'


class PlayerBattleUnit(models.Model):
    in_deck = models.BooleanField(default=False)
    on_market = models.BooleanField(default=False)
    market_price = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    health_points = models.IntegerField(blank=True, null=True)
    attack_points = models.IntegerField(blank=True, null=True)
    shield_level = models.IntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    base_unit = models.ForeignKey(BattleUnit, on_delete=models.CASCADE, null=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Персонаж игрока'
        verbose_name_plural = 'Персонажи игрока'


class BattleHistory(models.Model):
    result = models.CharField(max_length=30, blank=True, verbose_name='Результат')
    enemy_game_name = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.time_create

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'История'
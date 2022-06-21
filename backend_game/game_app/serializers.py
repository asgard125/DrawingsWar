from rest_framework import serializers
from .models import *


class PublicUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('game_name', 'level_score', 'rating', 'wins', 'defeats')


class SelfUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('game_name', 'level_score', 'rating', 'wins', 'defeats', 'username', 'money', 'deck_size', 'units_in_deck')


class BattleUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleUnit
        fields = '__all__'


class PlayerBattleUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerBattleUnit
        fields = '__all__'


class BattleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleHistory
        fields = '__all__'


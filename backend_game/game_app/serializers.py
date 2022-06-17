from rest_framework import serializers
from .models import BattleUnit




class BattleUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleUnit
        fields = '__all__'

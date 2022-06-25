from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import *
from rest_framework.response import Response
from .permissions import IsCurrentUser
from .serializers import *


class BattleUnitAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = BattleUnit.objects.all()
    serializer_class = BattleUnitSerializer
    permission_classes = (IsAuthenticated, )


class PlayerBattleUnitAPIView(GenericViewSet):
    queryset = PlayerBattleUnit.objects.all()

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'upgrade'):
            permission_classes = [IsCurrentUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = PlayerBattleUnit.objects.filter(user=request.user)
        serializer = PlayerBattleUnitSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if 'id' in request.data:
            if request.data['id'].isdigit():
                base_unit = get_object_or_404(BattleUnit, pk=int(request.data['id']))
            else:
                return Response({'status': 'fail', 'details': 'wrong base unit id'})
        else:
            return Response({'status': 'fail', 'details': 'wrong base unit id'})

        if base_unit.shop_price > request.user.money:
            return Response({'status': 'fail', 'details': 'not enough money'})

        if base_unit.start_level_buy > request.user.level_score // 100:
            return Response({'status': 'fail', 'details': 'user level is too low'})

        PlayerBattleUnit.buy_unit_in_shop(request.user, base_unit)
        return Response({'status': 'ok', 'details': 'ok'})

    def retrieve(self, request, pk=None):
        playerunit = get_object_or_404(PlayerBattleUnit, pk=pk)
        serializer = PlayerBattleUnitSerializer(playerunit, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def upgrade(self, request, pk=None):
        playerunit = get_object_or_404(PlayerBattleUnit, pk=pk)
        if request.user.money < playerunit.upgrade_price:
            return Response({'status': 'fail', 'details': 'not enough money'})
        PlayerBattleUnit.upgrade_unit(request.user, playerunit)
        return Response({'status': 'ok', 'details': 'ok'})

    @action(detail=False, methods=['put'])
    def market_purchase(self, request):
        if 'id' in request.data:
            if request.data['id'].isdigit():
                playerunit = get_object_or_404(PlayerBattleUnit, pk=int(request.data['id']))
            else:
                return Response({'status': 'fail', 'details': 'wrong base unit id'})
        else:
            return Response({'status': 'fail', 'details': 'wrong base unit id'})
        if request.user == playerunit.user:
            return Response({'status': 'fail', 'details': 'cannot buy yourself unit'})
        if request.user.money < playerunit.market_price:
            return Response({'status': 'fail', 'details': 'not enough money'})
        request.user.money = request.user.money - playerunit.market_price  # изменение денег для покупателя
        playerunit.user.money = playerunit.user.money + playerunit.market_price  # изменение денег для продавца
        playerunit.user = request.user  # изменение владельца юнита
        playerunit.on_market = False
        request.user.save()
        playerunit.save()
        return Response({'status': 'ok', 'details': 'ok'})

    @action(detail=False, methods=['get'])
    def market_list(self, request):
        queryset = PlayerBattleUnit.objects.filter(on_market=True)
        serializer = PlayerBattleUnitSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        playerunit = get_object_or_404(PlayerBattleUnit, pk=pk)
        if 'action' not in request.data:
            return Response({'status': 'fail', 'details': 'action is required'})
        if request.data['action'] == 'set_on_market':
            playerunit.on_market = True
            if playerunit.in_deck:
                playerunit.in_deck = False
                playerunit.user.units_in_deck = playerunit.user.units_in_deck - 1
            if 'market_price' not in request.data:
                return Response({'status': 'fail', 'details': 'wrong market price'})
            if not request.data['market_price'].isdigit():
                return Response({'status': 'fail', 'details': 'wrong market price'})
            playerunit.market_price = int(request.data['market_price'])
            playerunit.save()
        elif request.data['action'] == 'delete_from_market':
            playerunit.on_market = False
            playerunit.save()
        elif request.data['action'] == 'set_in_deck':
            if playerunit.on_market:
                return Response({'status': 'fail', 'details': 'unit is on market'})
            playerunit.in_deck = True
            playerunit.user.units_in_deck = playerunit.user.units_in_deck + 1
            playerunit.save()
        return Response({'status': 'ok', 'details': 'ok'})


class BattleHistoryAPIView(GenericViewSet):
    queryset = BattleHistory.objects.all()
    permission_classes = (IsCurrentUser,)

    def list(self, request):
        history = BattleHistory.objects.filter(user=request.user, order_by='-time_create')
        serializer = BattleHistorySerializer(history, many=False)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        history = get_object_or_404(BattleHistory, pk=pk)
        serializer = BattleHistorySerializer(history, many=False)
        return Response(serializer.data)


class UserAPIView(GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            permission_classes = [IsCurrentUser]
        elif self.action in ('destroy', 'create'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = User.objects.all().order_by('-rating')
        serializer = PublicUserDataSerializer(queryset, many=True)
        return Response({'users': serializer.data})

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = PublicUserDataSerializer(user, many=False)
        return Response({'user': serializer.data})

    @action(methods=['get'], detail=False)
    def current_user(self, request):
        serializer = SelfUserDataSerializer(request.user, many=False)
        return Response({'user': serializer.data})



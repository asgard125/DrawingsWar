import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from battle_app.engine import GameEngine
from battle_app.models import BattleSession
from game_app.models import PlayerBattleUnit
from game_app.serializers import *


def _get_user_deck(user=None):
    queryset = PlayerBattleUnit.objects.filter(user=user, in_deck=True)
    return PlayerBattleUnitSerializer(queryset, many=True).data


def _is_room_exist_and_available(room_code=None):
    rooms = BattleSession.objects.filter(room_code=room_code)
    rooms = [obj for obj in rooms if obj.players_count < 2]
    return len(rooms) > 0


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_is_available = await sync_to_async(_is_room_exist_and_available, thread_sensitive=True)(room_code=self.scope['url_route']['kwargs']['room_name'])
        if room_is_available and not self.scope['user'].is_anonymous:

            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'room_%s' % self.room_name
            self.user_deck = await sync_to_async(_get_user_deck, thread_sensitive=True)(user=self.scope['user'])
            self.user_game_name = self.scope['user'].game_name
            self.user_rating = self.scope['user'].rating
            self.user_id = self.scope['user'].id

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            print('User connected')
            print('joined new player')
            await self.channel_layer.send(
                "game_engine",
                {"type": "player.new", 'room_code': self.room_name, "game_name": self.user_game_name, "channel": self.channel_name,
                 'group_name': self.room_group_name, 'deck': self.user_deck, 'rating': self.user_rating,
                 'player_id': self.user_id},
            )

    async def disconnect(self, close_code):
        print('user left')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        content = json.loads(text_data)
        await self.channel_layer.send(
            "game_engine",
            {"type": "player.event", 'data': content['data']}
        )

    async def game_update(self, event):
        game = event["game"]
        await self.send(json.dumps(game))


class EngineConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = "base_group_name"
        self.engine = GameEngine(self.group_name)
        self.engine.start()

    def player_new(self, event):
        if self.group_name == "base_group_name":
            self.group_name = event['group_name']
            self.room_code = event['room_code']
            self.engine.group_name = self.group_name
        print("Player Joined: %s", event["game_name"])
        self.engine.handle_new_player(event)

    def player_event(self, event):
        self.engine.handle_player_event(event)
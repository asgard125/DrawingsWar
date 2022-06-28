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


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        rooms = await sync_to_async(BattleSession.objects.filter, thread_sensitive=True)(room_code=int(self.scope['url_route']['kwargs']['room_name']))
        rooms = await sync_to_async(len, thread_sensitive=True)(rooms)
        if rooms > 0:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'room_%s' % self.room_name
            self.user_deck = await sync_to_async(_get_user_deck, thread_sensitive=True)(user=self.scope['user'])
            self.user_game_name = self.scope['user'].game_name
            self.user_rating = self.scope['user'].rating
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            print('User connected')
            print('joined new player')
            await self.channel_layer.send(
                "game_engine",
                {"type": "player.new", "game_name": self.user_game_name, "channel": self.channel_name,
                 'group_name': self.room_group_name, 'deck': self.user_deck, 'rating': self.user_rating},
            )

    async def disconnect(self, close_code):
        print('user left')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from Websocket
    async def receive(self, text_data=None, bytes_data=None):
        content = json.loads(text_data)
        print(content)

    # Send game data to room group after a Tick is processed
    async def game_update(self, event):
        print("Game Update, timer, player_turn", event['timer'], event['player_turn'])
        # Send message to WebSocket
        state = event["state"]
        await self.send(json.dumps(state))


class EngineConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = "base_group_name"
        self.engine = GameEngine(self.group_name)
        self.engine.start()

    def player_new(self, event):
        if self.group_name == "base_group_name":
            self.group_name = event['group_name']
            self.engine.group_name = self.group_name
        print(event["deck"])
        print("Player Joined: %s", event["game_name"])

    def player_event(self, event):
        pass
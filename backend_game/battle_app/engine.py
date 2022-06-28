import threading
import time
from collections import OrderedDict

import attr
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Unit:
    def __init__(self, x=None, y=None, health_points=None, attack_points=None, shield_level=None,
                 max_move_range=None, max_attack_range=None, battle_class=None):
        self.x = x
        self.y = y
        self.health_points = health_points
        self.attack_points = attack_points
        self.shield_level = shield_level
        self.max_move_range = max_move_range
        self.max_attack_range = max_attack_range
        self.battle_class = battle_class


class Player:
    def __init__(self, game_name=None, rating=None, player_id=None, turn=None):
        self.turn = turn
        self.player_id = player_id
        self.game_name = game_name
        self.rating = rating
        self.deck = []

    def add_deck(self, deck):
        pass

    def unit_in_cords(self, x, y):
        for unit in self.deck:
            if unit.x == x and unit.y == y:
                return True
        return False


class GameEngine(threading.Thread):
    move_time = 16
    tick_rate = 1
    player_count = 2
    x_dim = 5
    y_dim = 10

    def __init__(self, group_name, **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.timer = 0
        self.player_turn = 0
        self.group_name = group_name
        self.players_in_group = 1
        self.board = [[None for _ in range(self.x_dim)] for i in range(self.y_dim)]
        self.has_changes = False
        self.game_state = {}
        self.player_queue = OrderedDict()
        self.channel_layer = get_channel_layer()
        self.player_lock = threading.Lock()

    def run(self) -> None:
        print('game engine started', self.group_name)
        while True:
            # смена хода, обработка действий
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "game.update", "state": 'kek', "timer": self.timer + 1,
                                  "player_turn": self.player_turn + 1}
            )
            time.sleep(self.tick_rate)
            self.timer = (self.timer + self.tick_rate) % self.move_time
            if self.timer == 0:
                self.player_turn = (self.player_turn + 1) % self.player_count

    def send_game_board_state(self):
        state_json = {
            'event': 'no',
            'board': 'no'
        }
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "game_update", "state": state_json}
        )
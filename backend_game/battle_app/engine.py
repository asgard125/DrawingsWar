import threading
import time
from collections import OrderedDict

import attr
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Unit:
    def __init__(self, owner_id=None, x=None, y=None, health_points=None, attack_points=None, shield_level=None,
                 max_move_range=None, max_attack_range=None, battle_class=None, name=None):
        self.owner_id = owner_id
        self.x = x
        self.y = y
        self.health_points = health_points
        self.attack_points = attack_points
        self.shield_level = shield_level
        self.max_move_range = max_move_range
        self.max_attack_range = max_attack_range
        self.battle_class = battle_class
        self.name = name

    def render(self):
        return {'unit':
                    {
                     'x': self.x,
                     'y': self.y,
                     'health_points': self.health_points,
                     'attack_points': self.attack_points,
                     'shield_level': self.shield_level,
                     'max_move_range': self.max_move_range,
                     'max_attack_range': self.max_attack_range,
                     'battle_class': self.battle_class,
                     'name': self.name,
                     'owner_id': self.owner_id
                    }
                }


class Player:
    def __init__(self, game_name=None, rating=None, player_id=None, turn=None):
        self.turn = turn
        self.player_id = player_id
        self.game_name = game_name
        self.rating = rating


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
        self.game_state = 'waiting'
        self.players = []
        self.winner = None
        self.channel_layer = get_channel_layer()
        self.player_lock = threading.Lock()

    def handle_new_player(self, data):
        pass

    def handle_player_event(self, data):
        pass

    def run(self) -> None:
        print('game engine started', self.group_name)
        while True:
            # смена хода, обработка действий
            if self.game_state == 'started':
                self.send_game_state()
                self.timer = (self.timer + self.tick_rate) % self.move_time
                if self.timer == 0:
                    self.player_turn = (self.player_turn + 1) % self.player_count
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name, {"type": "game.update", 'game': {"state": self.game_state, 'winner': self.winner}}
                )
            time.sleep(self.tick_rate)

    def send_game_state(self):
        rendered_board = []
        for layer in self.board:
            rendered_board.append([i.render() if i is not None else i for i in layer])
        state_json = {"type": "game.update", 'game': {
                        "state": self.game_state, "timer": self.timer + 1,
                        "board": rendered_board, "player_turn": self.player_turn}}
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, state_json
        )

    def check_win(self):
        pass
import threading
import time
from collections import OrderedDict

from battle_app.models import BattleSession
from game_app import game_consts
from game_app.models import User, BattleHistory

import attr
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Unit:
    def __init__(self, player_id=None, x=None, y=None, health_points=None, attack_points=None, shield_level=None,
                 max_move_range=None, max_attack_range=None, battle_class=None, name=None):
        self.player_id = int(player_id)
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
        self.player_id = int(player_id)
        self.game_name = game_name
        self.rating = rating


class Board:
    def __init__(self, x_dim=None, y_dim=None):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.board = [[None for _ in range(self.x_dim)] for i in range(self.y_dim)]

    def player_attack_on(self, player_id=None, s_x=None, s_y=None, m_x=None, m_y=None):
        if self.board[s_y][s_x] is None:
            return False
        elif self.board[s_y][s_x].player_id != player_id:
            return False
        elif self.board[m_y][m_x] is None:
            return False
        elif self.board[m_y][m_x].player_id == player_id:
            return False
        elif (abs(m_x - s_x) > self.board[s_y][s_x].max_attack_range or
            abs(m_y - s_y) > self.board[s_y][s_x].max_attack_range):
            return False
        if self.board[m_y][m_x].shield_level > 0:
            self.board[m_y][m_x].health_points -= self.board[s_y][s_x].attack_points / 1.2
            self.board[m_y][m_x].shield_level //= 2
        else:
            self.board[m_y][m_x].health_points -= self.board[s_y][s_x].attack_points
        if self.board[m_y][m_x].health_points <= 0:
            self.board[m_y][m_x] = None
        return True

    def player_move_on(self, player_id=None, s_x=None, s_y=None, m_x=None, m_y=None):
        if self.board[s_y][s_x] is None:
            return False
        elif self.board[s_y][s_x].player_id != player_id:
            return False
        elif (abs(m_x - s_x) > self.board[s_y][s_x].max_move_range or
            abs(m_y - s_y) > self.board[s_y][s_x].max_move_range) or (m_y == s_y and m_x == s_x):
            return False
        # horizontal check
        if m_y == s_y:
            for x in range(min(m_x, s_x), max(m_x, s_x) + 1):
                if self.board[s_y][x] is not None and x != s_x:
                    return False
        # vertical check
        if m_x == s_x:
            for y in range(min(m_y, s_y), max(m_y, s_y) + 1):
                if self.board[y][s_x] is not None and y != s_y:
                    return False

        self.board[s_y][s_x].x = m_x
        self.board[s_y][s_x].y = m_y
        return True

    def render(self):
        rendered_board = []
        for layer in self.board:
            rendered_board.append([i.render() if i is not None else i for i in layer])
        return rendered_board


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
        self.room_code = None
        self.players_in_group = 0
        self.board = Board(x_dim=self.x_dim, y_dim=self.y_dim)
        self.has_changes = False
        self.game_state = 'waiting'
        self.players = []
        self.winner = {'player_id': None, 'player_game_name': None}
        self.channel_layer = get_channel_layer()
        self.player_lock = threading.Lock()

    def handle_new_player(self, data):
        new_player = Player(game_name=data['game_name'], player_id=data['player_id'], rating=data['rating'], turn=self.players_in_group)
        self.players_in_group += 1
        self.players.append(new_player)
        layer = 0
        if self.players_in_group == 1:
            border_pos = 0
        elif self.players_in_group == 2:
            self.game_state = 'started'
            border_pos = self.x_dim - 1
        for unit in data['deck']:
            self.board.board[layer][border_pos] = Unit(y=layer, x=border_pos, health_points=unit['health_points'],
                                            attack_points=unit['attack_points'], shield_level=unit['shield_level'],
                                            max_move_range=unit['base_unit']['max_move_range'],
                                            max_attack_range=unit['base_unit']['max_attack_range'],
                                            battle_class=unit['base_unit']['battle_class'],
                                            name=unit['base_unit']['name'], player_id=data['player_id'])
            layer += 1

    def handle_player_event(self, event):
        player_id = int(event['data']['player_id'])
        event_type = event['data']['type']
        selected_x = int(event['data']['selected']['x'])
        selected_y = int(event['data']['selected']['y'])
        move_x = int(event['data']['move']['x'])
        move_y = int(event['data']['move']['y'])
        room = BattleSession.objects.get(room_code=self.room_code)
        room.players_count += 1
        room.save()
        if event_type == 'move' and self.players[self.player_turn].player_id == player_id:
            if self.board.player_attack_on(player_id=player_id, s_x=selected_x, s_y=selected_y, m_x=move_x, m_y=move_y):
                self.timer = 0
                self.player_turn = (self.player_turn + 1) % self.player_count
            elif self.board.player_move_on(player_id=player_id, s_x=selected_x, s_y=selected_y, m_x=move_x, m_y=move_y):
                self.timer = 0
                self.player_turn = (self.player_turn + 1) % self.player_count
        self.handle_win()

    def run(self) -> None:
        print('game engine started', self.group_name)
        while True:
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
        print(self.player_turn)
        state_json = {"type": "game.update", 'game': {
                        "state": self.game_state, "timer": self.timer + 1,
                        "board": self.board.render(), "player_id_turn": self.players[self.player_turn].player_id}}
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, state_json
        )

    def handle_win(self):
        player1_units_on_board = 0
        player2_units_on_board = 0
        for layer in range(self.y_dim):
            for cell in range(self.x_dim):
                if self.board.board[layer][cell] is not None:
                    if int(self.board.board[layer][cell].player_id) == int(self.players[0].player_id):
                        player1_units_on_board += 1
                    else:
                        player2_units_on_board += 1
        if player1_units_on_board == 0:
            self.game_state = 'over'
            self.winner['player_id'] = self.players[1].player_id
            self.winner['player_game_name'] = self.players[1].game_name
            winner_user = User.objects.get(pk=int(self.players[1].player_id))
            looser_user = User.objects.get(pk=int(self.players[0].player_id))
            winner_user.update_after_battle(result='win')
            looser_user.update_after_battle(result='loose')
            winner_history = BattleHistory(result='win', user=winner_user, enemy_game_name=looser_user.game_name)
            looser_history = BattleHistory(result='loose', user=looser_user, enemy_game_name=winner_user.game_name)
            winner_history.save()
            looser_history.save()
            room = BattleSession.objects.get(room_code=self.room_code)
            room.delete()
        elif player2_units_on_board == 0:
            self.game_state = 'over'
            self.winner['player_id'] = self.players[0].player_id
            self.winner['player_game_name'] = self.players[0].game_name
            winner_user = User.objects.get(pk=int(self.players[0].player_id))
            looser_user = User.objects.get(pk=int(self.players[1].player_id))
            winner_user.update_after_battle(result='win')
            looser_user.update_after_battle(result='loose')
            winner_history = BattleHistory(result='win', user=winner_user, enemy_game_name=looser_user.game_name)
            looser_history = BattleHistory(result='loose', user=looser_user, enemy_game_name=winner_user.game_name)
            winner_history.save()
            looser_history.save()
            room = BattleSession.objects.get(room_code=self.room_code)
            room.delete()



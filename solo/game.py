from player import Player
from board import Board
import random

class Game:
    def __init__(self, role, rows=5, cols=5, nb_obstacles=5, max_turns=10, turn_time=10):
        while True:
            self.board = Board(rows, cols, nb_obstacles)
            self.role = role
            self.rows = rows
            self.cols = cols
            self.max_turns = max_turns
            self.turn_time = turn_time

            self.player = Player("joueur", role, self.random_position())
            pnj_role = "wolf" if role == "villager" else "villager"
            self.pnj = Player("pnj", pnj_role, self.random_position(exclude=self.player.position))

            # Supprimer les obstacles sous les joueurs
            self.board.obstacles.discard(self.player.position)
            self.board.obstacles.discard(self.pnj.position)

            if not self.is_player_blocked():
                break  # Joueur a au moins une sortie

    def random_position(self, exclude=None):
        while True:
            pos = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            if pos != exclude and pos not in self.board.obstacles:
                return pos

    def is_player_blocked(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        row, col = self.player.position
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if (r, c) not in self.board.obstacles:
                    return False
        return True

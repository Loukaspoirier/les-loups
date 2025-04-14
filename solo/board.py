import random

class Board:
    def __init__(self, rows, cols, nb_obstacles=5):
        self.rows = rows
        self.cols = cols
        self.obstacles = set()
        self.generate_obstacles(nb_obstacles)

    def generate_obstacles(self, count):
        while len(self.obstacles) < count:
            pos = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            self.obstacles.add(pos)

    def display(self, player, pnj):
        print("\nPlateau :")
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                pos = (i, j)
                if pos == player.position:
                    row += " P "
                elif pos == pnj.position:
                    row += " N "
                elif pos in self.obstacles:
                    row += " X "
                else:
                    row += " . "
            print(row)

    def is_obstacle(self, position):
        return position in self.obstacles

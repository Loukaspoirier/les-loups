class Player:
    def __init__(self, name, role, position):
        self.name = name
        self.role = role  # "wolf" ou "villager"
        self.position = position  # (row, col)

    def move(self, direction, max_rows, max_cols, is_blocked_func):
        row, col = self.position
        new_row, new_col = row, col

        if direction == "up":
            new_row -= 1
        elif direction == "down":
            new_row += 1
        elif direction == "left":
            new_col -= 1
        elif direction == "right":
            new_col += 1
        else:
            print("Commande inconnue.")
            return

        # Vérifie les limites du plateau
        if 0 <= new_row < max_rows and 0 <= new_col < max_cols:
            if is_blocked_func((new_row, new_col)):
                print("❌ Déplacement bloqué par un obstacle !")
            else:
                self.position = (new_row, new_col)
        else:
            print("❌ Déplacement invalide, hors du plateau.")

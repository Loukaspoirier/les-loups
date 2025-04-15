import random

# Paramètres de la grille
GRID_SIZE = 5

# Initialisation du plateau
def create_grid(player_pos, npc_pos):
    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    x, y = player_pos
    grid[y][x] = "P"  # P = Player
    x, y = npc_pos
    grid[y][x] = "N"  # N = NPC
    return grid

# Affichage du plateau
def print_grid(grid):
    for row in grid:
        print(" ".join(row))
    print()

# Déplacement du joueur
def move_player(pos, direction):
    x, y = pos
    if direction == "z" and y > 0:
        y -= 1
    elif direction == "s" and y < GRID_SIZE - 1:
        y += 1
    elif direction == "q" and x > 0:
        x -= 1
    elif direction == "d" and x < GRID_SIZE - 1:
        x += 1
    return (x, y)

# Lancement du jeu
def main():
    print("Bienvenue dans la version solo de Loup-Garou !")
    role = input("Choisissez votre rôle (loup / villageois) : ").strip().lower()
    
    if role not in ["loup", "villageois"]:
        print("Rôle invalide.")
        return

    player_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    
    # Générer une position différente pour le PNJ
    while True:
        npc_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if npc_pos != player_pos:
            break

    print(f"Vous êtes le {role}.")
    print("Déplacez-vous avec Z (haut), Q (gauche), S (bas), D (droite).")

    while True:
        grid = create_grid(player_pos, npc_pos)
        print_grid(grid)

        if role == "loup" and player_pos == npc_pos:
            print("Vous avez éliminé le villageois. Victoire ! 🐺")
            break
        elif role == "villageois" and player_pos == npc_pos:
            print("Le loup vous a eu... Défaite. 🧑‍🌾")
            break

        move = input("Votre déplacement (z/q/s/d) : ").lower()
        if move in ["z", "q", "s", "d"]:
            player_pos = move_player(player_pos, move)
        else:
            print("Commande invalide.")

if __name__ == "__main__":
    main()

import requests
import json
import os

def main():
    print("=== Création d'une partie ===")

    # Lecture des variables d'environnement avec valeurs par défaut
    title = os.getenv("PARTY_TITLE", "Titre par défaut")
    map_width = int(os.getenv("MAP_WIDTH", 10))
    map_height = int(os.getenv("MAP_HEIGHT", 10))
    nb_players = int(os.getenv("NB_PLAYERS", 4))
    max_turns = int(os.getenv("MAX_TURNS", 20))
    turn_duration_seconds = int(os.getenv("TURN_DURATION", 30))
    nb_obstacles = int(os.getenv("NB_OBSTACLES", 5))

    data = {
        "title": title,
        "map_width": map_width,
        "map_height": map_height,
        "nb_players": nb_players,
        "max_turns": max_turns,
        "turn_duration_seconds": turn_duration_seconds,
        "nb_obstacles": nb_obstacles
    }

    try:
        response = requests.post("http://localhost:5001/create-party", json=data)
        if response.status_code == 200:
            print("✅ Partie créée avec succès !")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Erreur lors de la création :", response.status_code)
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("❌ Erreur de connexion au serveur :", e)

if __name__ == "__main__":
    main()

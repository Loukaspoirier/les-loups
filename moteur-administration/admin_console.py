import requests
import json

def main():
    print("=== Création d'une partie ===")
    title = input("Titre de la partie : ")
    map_width = int(input("Largeur de la carte : "))
    map_height = int(input("Hauteur de la carte : "))
    nb_players = int(input("Nombre de joueurs : "))
    max_turns = int(input("Nombre maximal de tours : "))
    turn_duration_seconds = int(input("Durée d’un tour (en secondes) : "))
    nb_obstacles = int(input("Nombre d’obstacles : "))

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
        response = requests.post("http://localhost:8000/create-party", json=data)
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
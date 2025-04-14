import requests

BASE_URL = "http://localhost:5432/"


def creer_partie():
    print("\n=== Création d'une partie ===")
    nb_lignes = int(input("Nombre de lignes : "))
    nb_colonnes = int(input("Nombre de colonnes : "))
    nb_tours = int(input("Nombre de tours max : "))
    delai = int(input("Temps d'un tour (secondes) : "))
    nb_obstacles = int(input("Nombre d'obstacles : "))
    max_joueurs = int(input("Nombre maximum de joueurs : "))
    resultat = creer_partie_api(nb_lignes, nb_colonnes, nb_tours, delai, nb_obstacles, max_joueurs)
    print(resultat)

def creer_partie_api(nb_lignes, nb_colonnes, nb_tours, delai, nb_obstacles, max_joueurs):
    data = {
        "nb_lignes": nb_lignes,
        "nb_colonnes": nb_colonnes,
        "nb_tours": nb_tours,
        "delai": delai,
        "nb_obstacles": nb_obstacles,
        "max_joueurs": max_joueurs
    }
    try:
        response = requests.post(f"{BASE_URL}/partie", json=data)
        return response.json()
    except Exception as e:
        return {"erreur": str(e)}
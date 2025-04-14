import requests

BASE_URL = "http://localhost:5000"

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

def inscription_api(id_partie, nom):
    try:
        response = requests.post(f"{BASE_URL}/partie/{id_partie}/inscription", json={"nom": nom})
        return response.json()
    except Exception as e:
        return {"erreur": str(e)}

def etat_partie_api(id_partie):
    try:
        response = requests.get(f"{BASE_URL}/partie/{id_partie}/etat")
        return response.json()
    except Exception as e:
        return {"erreur": str(e)}

def lister_parties_api():
    try:
        response = requests.get(f"{BASE_URL}/parties")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"erreur": str(e)}

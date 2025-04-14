import requests

BASE_URL = "http://serveur:5000"

def creer_partie():
    print("\n=== Création d'une partie ===")
    data = {
        "nb_lignes": int(input("Nombre de lignes : ")),
        "nb_colonnes": int(input("Nombre de colonnes : ")),
        "nb_tours": int(input("Nombre de tours max : ")),
        "delai": int(input("Temps d'un tour (secondes) : ")),
        "nb_obstacles": int(input("Nombre d'obstacles : ")),
        "max_joueurs": int(input("Nombre maximum de joueurs : "))
    }
    response = requests.post(f"{BASE_URL}/partie", json=data)
    print(response.json())

def inscription():
    print("\n=== Inscription à une partie ===")
    id_partie = input("ID de la partie : ")
    nom = input("Nom du joueur : ")
    response = requests.post(f"{BASE_URL}/partie/{id_partie}/inscription", json={"nom": nom})
    print(response.json())

def etat_partie():
    print("\n=== État d'une partie ===")
    id_partie = input("ID de la partie : ")
    response = requests.get(f"{BASE_URL}/partie/{id_partie}/etat")
    print(response.json())

def lister_parties():
    print("\n=== Liste des parties ===")
    try:
        response = requests.get(f"{BASE_URL}/parties")
        response.raise_for_status()
        parties = response.json()
        if not parties:
            print("Aucune partie disponible.")
        for partie in parties:
            print(f"ID: {partie['id']} | État: {partie['etat']} | Joueurs: {len(partie['joueurs'])} | Config: {partie['config']}")
    except Exception as e:
        print("Erreur lors de la récupération des parties :", e)

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Créer une partie")
        print("2. S'inscrire à une partie")
        print("3. Voir l'état d'une partie")
        print("4. Lister les parties")
        print("5. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            creer_partie()
        elif choix == "2":
            inscription()
        elif choix == "3":
            etat_partie()
        elif choix == "4":
            lister_parties()
        elif choix == "5":
            print("À bientôt !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()
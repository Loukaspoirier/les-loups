from function import creer_partie_api, inscription_api, etat_partie_api, lister_parties_api, deplacer_api;


def inscription():
    print("\n=== Inscription à une partie ===")
    id_partie = input("ID de la partie : ")
    nom = input("Nom du joueur : ")
    resultat = inscription_api(id_partie, nom)
    print(resultat)

def etat_partie():
    print("\n=== État d'une partie ===")
    id_partie = input("ID de la partie : ")
    resultat = etat_partie_api(id_partie)
    print(resultat)

def lister_parties():
    print("\n=== Liste des parties ===")
    parties = lister_parties_api()
    if "erreur" in parties:
        print("Erreur :", parties["erreur"])
    elif not parties:
        print("Aucune partie disponible.")
    else:
        for partie in parties:
            print(f"ID: {partie['id']} | État: {partie['etat']} | Joueurs: {len(partie['joueurs'])} | Config: {partie['config']}")


def deplacer():
    print("\n=== Déplacement ===")
    id_partie = input("ID de la partie : ")
    id_joueur = input("ID du joueur : ")
    print("Direction: 0=pas de mouvement, 1=haut/bas (lignes), -1=bas/haut (lignes)")
    ligne = input("Déplacement ligne (-1, 0, 1): ")
    colonne = input("Déplacement colonne (-1, 0, 1): ")
    direction = f"{ligne}{colonne}"  # Format "01"
    
    resultat = deplacer_api(id_partie, id_joueur, direction)
    print(resultat)

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. S'inscrire à une partie")
        print("2. Voir l'état d'une partie")
        print("3. Lister les parties")
        print("4. Se déplacer")
        print("5. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            inscription()
        elif choix == "2":
            etat_partie()
        elif choix == "3":
            lister_parties()
        elif choix == "4":
            deplacer()
        elif choix == "5":
            print("À bientôt !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()

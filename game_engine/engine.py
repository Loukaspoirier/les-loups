from db import SessionLocal
from models import Player, PlayerInParty, Party, PlayerPlay, Role
from datetime import datetime
from sqlalchemy import text

class GameEngineService:
    def __init__(self):
        self.db = SessionLocal()

    def enregistrer_joueur(self, pseudo, id_partie):
        # Création du joueur
        joueur = Player(pseudo=pseudo)
        self.db.add(joueur)
        self.db.commit()
        self.db.refresh(joueur)

        # Attribution d'un rôle aléatoire avec la fonction SQL
        requete_role = text("SELECT random_role(:id_partie) as role")
        resultat_role = self.db.execute(requete_role, {"id_partie": id_partie}).fetchone()
        nom_role = resultat_role.role
        
        # Récupération de l'ID du rôle
        role = self.db.query(Role).filter(Role.nom == nom_role).first()
        if not role:
            raise Exception(f"Rôle {nom_role} introuvable en base de données")

        # Association joueur-partie avec rôle
        joueur_partie = PlayerInParty(
            id_party=id_partie,
            id_player=joueur.id_player,
            id_role=role.id_role,
            is_alive=True
        )
        self.db.add(joueur_partie)
        self.db.commit()
        self.db.refresh(joueur_partie)

        return joueur.id_player

    def deplacer_joueur(self, id_joueur, colonne_origine, ligne_origine, colonne_cible, ligne_cible):
        joueur_partie = self.db.query(PlayerInParty).filter(PlayerInParty.id_player == id_joueur).first()
        if not joueur_partie:
            raise Exception("Joueur non trouvé dans la partie")

        # Récupération du tour actif
        requete_tour = text("""
            SELECT id_turn FROM turns 
            WHERE id_party = :id_partie AND statut = 'active' 
            ORDER BY id_turn DESC LIMIT 1
        """)
        resultat_tour = self.db.execute(requete_tour, {"id_partie": joueur_partie.id_party}).fetchone()
        
        if not resultat_tour:
            raise Exception("Aucun tour actif trouvé pour cette partie")
            
        id_tour = resultat_tour.id_turn

        # Enregistrement du déplacement
        action = PlayerPlay(
            id_players_in_parties=joueur_partie.id_players_in_parties,
            id_turn=id_tour,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            action="MOVE",
            origin_position_col=colonne_origine,
            origin_position_row=ligne_origine,
            target_position_col=colonne_cible,
            target_position_row=ligne_cible
        )
        self.db.add(action)
        self.db.commit()
        return True

    def terminer_tour(self, id_tour, id_partie):
        # Appel de la procédure stockée
        requete_terminer = text("CALL COMPLETE_TOUR(:id_tour, :id_partie)")
        self.db.execute(requete_terminer, {"id_tour": id_tour, "id_partie": id_partie})
        self.db.commit()
        return True

    def obtenir_info_vainqueur(self, id_partie):
        # Appel de la fonction SQL
        requete_vainqueur = text("""
            SELECT * FROM get_the_winner(:id_partie)
        """)
        resultat = self.db.execute(requete_vainqueur, {"id_partie": id_partie}).fetchone()
        
        if not resultat:
            raise Exception("Aucun vainqueur trouvé pour cette partie")
            
        return {
            "nom_joueur": resultat.nom_joueur,
            "role": resultat.role,
            "nom_partie": resultat.nom_partie,
            "tours_joues": resultat.nb_tours_joues,
            "tours_totaux": resultat.nb_total_tours,
            "temps_moyen_decision": resultat.temps_moyen_prise_decision
        }
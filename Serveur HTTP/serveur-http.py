from flask import Flask, request, jsonify

app = Flask(__name__)

# === Simulation du moteur de jeu (via gRPC normalement) ===
class MoteurStub:
    def __init__(self):
        self.parties = {}
        self.id_counter = 1

    def creer_partie(self, config):
        id_partie = self.id_counter
        self.id_counter += 1
        self.parties[id_partie] = {
            "id": id_partie,
            "config": config,
            "joueurs": [],
            "etat": "en_attente"
        }
        return self.parties[id_partie]

    def inscrire_joueur(self, id_partie, joueur):
        if id_partie in self.parties:
            self.parties[id_partie]["joueurs"].append(joueur)
            return {"message": "Joueur inscrit"}
        return {"erreur": "Partie introuvable"}

    def get_etat(self, id_partie):
        return self.parties.get(id_partie, {"erreur": "Partie introuvable"})

    def lister_parties(self):
        return list(self.parties.values())

moteur = MoteurStub()

# === Endpoints HTTP ===
@app.route("/partie", methods=["POST"])
def creer_partie():
    data = request.get_json()
    partie = moteur.creer_partie(data)
    return jsonify(partie), 201

@app.route("/partie/<int:id_partie>/inscription", methods=["POST"])
def inscription(id_partie):
    data = request.get_json()
    joueur = data.get("nom")
    resultat = moteur.inscrire_joueur(id_partie, joueur)
    return jsonify(resultat)

@app.route("/partie/<int:id_partie>/etat", methods=["GET"])
def etat_partie(id_partie):
    etat = moteur.get_etat(id_partie)
    return jsonify(etat)

@app.route("/parties", methods=["GET"])
def lister_parties():
    parties = moteur.lister_parties()
    return jsonify(parties)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

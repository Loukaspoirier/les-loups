import socket
import json
from threading import Thread

class ServeurTCP:
    def __init__(self, host='0.0.0.0', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.parties = {}  # Simule la BDD (comme dans le serveur HTTP)
        self.id_counter = 1

    def start(self):
        self.socket.listen(5)
        print(f"Serveur TCP en écoute sur {self.socket.getsockname()}")
        while True:
            client, addr = self.socket.accept()
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        try:
            data = client.recv(1024).decode()
            request = json.loads(data)
            response = self.traiter_requete(request)
            client.send(json.dumps(response).encode())
        except Exception as e:
            client.send(json.dumps({"status": "KO", "erreur": str(e)}).encode())
        finally:
            client.close()

    def traiter_requete(self, request):
        action = request.get("action")
        if action == "list":
            return self.lister_parties()
        elif action == "subscribe":
            return self.inscrire_joueur(request["parameters"])
        elif action == "move":
            return self.deplacer_joueur(request["parameters"])
        else:
            return {"status": "KO", "erreur": "Action non supportée"}

    def lister_parties(self):
        return {
            "status": "OK",
            "response": {"id_parties": list(self.parties.keys())}
        }

    def inscrire_joueur(self, params):
        id_partie = params[1]["id_party"]
        joueur = params[0]["player"]
        
        if id_partie not in self.parties:
            return {"status": "KO", "erreur": "Partie introuvable"}
        
        self.parties[id_partie]["joueurs"].append(joueur)
        return {
            "status": "OK",
            "response": {
                "role": "wolf" if len(self.parties[id_partie]["joueurs"]) % 2 else "villager",
                "id_player": len(self.parties[id_partie]["joueurs"])
            }
        }

    def deplacer_joueur(self, params):
        return {
            "status": "OK",
            "response": {
                "round_in_progress": 1,
                "move": {"next_position": {"row": 0, "col": 0}}
            }
        }

if __name__ == "__main__":
    serveur = ServeurTCP()
    serveur.start()
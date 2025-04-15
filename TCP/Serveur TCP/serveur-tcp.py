import socket
import json
import sys, os
from threading import Thread
# Définir le chemin relatif sous forme de chaîne de caractères
chemin_relatif = '../../game_engine/'

# Obtenir le chemin absolu et l'ajouter à sys.path
chemin_absolu = os.path.abspath(chemin_relatif)
sys.path.append(chemin_absolu)
print(sys.path.append(chemin_absolu))
# Maintenant, tu peux importer le fichier
from engine_pb2 import *
from engine_pb2_grpc import *

import grpc

from concurrent import futures
import time

class ServeurTCP:
    def __init__(self, host='0.0.0.0', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.grpc_channel = grpc.insecure_channel("localhost:50051")
        self.engine_stub = GameEngineStub(self.grpc_channel)

    def start(self):
        self.socket.listen(5)
        print(f"Serveur TCP en écoute sur {self.socket.getsockname()}")
        while True:
            client, addr = self.socket.accept()
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        try:
            data = client.recv(2048).decode()
            request = json.loads(data)
            response = self.traiter_requete(request)
            client.send(json.dumps(response).encode())
        except Exception as e:
            client.send(json.dumps({
                "status": "KO", 
                "erreur": str(e)
            }).encode())
        finally:
            client.close()

    def traiter_requete(self, request):
        action = request.get("action")
        parameters = request.get("parameters", [])
        
        if action == "list":
            return {"status": "OK", "response": {"id_parties": [1, 2, 3]}}
            
        elif action == "subscribe":
            player = next((p for p in parameters if "player" in p), {}).get("player")
            party_id = next((p for p in parameters if "id_party" in p), {}).get("id_party")
            print(player)
            print(party_id)
            grpc_response = self.engine_stub.RegisterPlayer(
                RegisterPlayerRequest(
                    pseudo=player,
                    party_id=int(party_id)
                )
            )
            return {
                "status": "OK",
                "response": {
                    "role": "wolf",
                    "id_player": grpc_response.player_id
                }
            }
            
        elif action == "move":
            player_id = next((p for p in parameters if "id_player" in p), {}).get("id_player")
            move = next((p for p in parameters if "move" in p), {}).get("move")
            
            grpc_response = self.engine_stub.MovePlayer(
                MovePlayerRequest(
                    player_id=int(player_id),
                    origin_position_col="0",
                    origin_position_row="0",
                    target_position_col=move[0],
                    target_position_row=move[1]
                )
            )
            return {
                "status": "OK",
                "response": {
                    "round_in_progress": 1,
                    "move": {
                        "next_position": {
                            "row": move[1],
                            "col": move[0]
                        }
                    }
                }
            }
            
        return {"status": "KO", "erreur": "Action non supportée"}

if __name__ == "__main__":
    ServeurTCP().start()
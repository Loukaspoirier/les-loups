import socket
import json

# Dictionnaire pour stocker les informations des joueurs
players = {}
player_counter = 1  # Compteur pour l'ID des joueurs
parties = {1: {"started": False}, 2: {"started": False}, 3: {"started": False}}  # Parties ouvertes

def handle_request(request):
    global player_counter

    # Parse la requête reçue
    try:
        request_data = json.loads(request)
    except json.JSONDecodeError:
        return json.dumps({"status": "KO", "response": "Invalid JSON"})
    
    action = request_data.get("action")
    parameters = request_data.get("parameters", [])

    if action == "list":
        # Retourner une liste de parties ouvertes non commencées
        open_parties = [party_id for party_id, party in parties.items() if not party["started"]]
        response = json.dumps({"status": "OK", "response": {"id_parties": open_parties}})
        return response

    elif action == "subscribe":
        if len(parameters) < 2:
            return json.dumps({"status": "KO", "response": "Missing parameters"})
        
        player_name = parameters[0].get('player')
        id_party = parameters[1].get('id_party')
        if not player_name or not id_party:
            return json.dumps({"status": "KO", "response": "Invalid player or party ID"})

        # S'inscrire à une partie
        player_id = player_counter
        players[player_id] = {
            "name": player_name,
            "id_party": id_party,
            "role": "villager"  # Par défaut, le joueur est un villageois
        }
        player_counter += 1  # Incrémenter l'ID pour le prochain joueur

        response = json.dumps({
            "status": "OK",
            "response": {
                "role": "villager",
                "id_player": player_id,
                "name": player_name
            }
        })
        return response

    elif action == "party_status":
        if len(parameters) < 2:
            return json.dumps({"status": "KO", "response": "Missing parameters"})
        
        player_id = parameters[0].get('id_player')
        party_id = parameters[1].get('id_party')
        if player_id not in players:
            return json.dumps({"status": "KO", "response": "Player not found"})
        
        player = players[player_id]
        response = json.dumps({
            "status": "OK",
            "response": {
                "party": {
                    "id_party": party_id,
                    "id_player": player_id,
                    "started": False,
                    "round_in_progress": 1,
                    "move": {
                        "next_position": {"row": 0, "col": 1}
                    }
                }
            }
        })
        return response

    elif action == "gameboard_status":
        if len(parameters) < 2:
            return json.dumps({"status": "KO", "response": "Missing parameters"})
        
        party_id = parameters[0].get('id_party')
        player_id = parameters[1].get('id_player')
        # Exemple de "plateau" visible (cela pourrait être dynamique dans une vraie application)
        visible_cells = "010010000"
        response = json.dumps({
            "status": "OK",
            "response": {
                "visible_cells": visible_cells
            }
        })
        return response

    elif action == "move":
        if len(parameters) < 3:
            return json.dumps({"status": "KO", "response": "Missing parameters"})
        
        party_id = parameters[0].get('id_party')
        player_id = parameters[1].get('id_player')
        move = parameters[2].get('move')
        # Appliquer le mouvement ici (exemple simplifié)
        response = json.dumps({
            "status": "OK",
            "response": {
                "round_in_progress": 1,
                "move": {
                    "next_position": {"row": 0, "col": 1}
                }
            }
        })
        return response
    
    return json.dumps({"status": "KO", "response": "Action non prise en charge"})

def start_server():
    host = '127.0.0.1'
    port = 54320  # Assurez-vous que ce port est disponible

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[+] Serveur TCP en écoute sur {host}:{port}\n")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[+] Nouveau client connecté : {client_address}\n")

        try:
            request = client_socket.recv(1024).decode('utf-8')
            if request:
                print(f"Requête reçue : {request}\n")
                response = handle_request(request)
                print(f"Réponse envoyée : {response}\n")
                client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors du traitement de la requête : {e}\n")
        finally:
            client_socket.close()
            print(f"[-] Client déconnecté : {client_address}\n")

if __name__ == '__main__':
    start_server()

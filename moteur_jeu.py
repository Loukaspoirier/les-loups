# moteur_jeu.py
import json

players = {}
player_counter = 1
parties = {1: {"started": False}, 2: {"started": False}, 3: {"started": False}}

def handle_request(request):
    global player_counter

    try:
        request_data = json.loads(request)
    except json.JSONDecodeError:
        return json.dumps({"status": "KO", "response": "Invalid JSON"})
    
    action = request_data.get("action")
    parameters = request_data.get("parameters", [])

    if action == "list":
        open_parties = [party_id for party_id, party in parties.items() if not party["started"]]
        return json.dumps({"status": "OK", "response": {"id_parties": open_parties}})

    elif action == "subscribe":
        if len(parameters) < 2:
            return json.dumps({"status": "KO", "response": "Missing parameters"})
        
        player_name = parameters[0].get('player')
        id_party = parameters[1].get('id_party')
        if not player_name or not id_party:
            return json.dumps({"status": "KO", "response": "Invalid player or party ID"})

        player_id = player_counter
        players[player_id] = {
            "name": player_name,
            "id_party": id_party,
            "role": "villager"
        }
        player_counter += 1

        return json.dumps({
            "status": "OK",
            "response": {
                "role": "villager",
                "id_player": player_id,
                "name": player_name
            }
        })

    elif action == "party_status":
        if len(parameters) < 2:
            return json.dumps({"status": "KO", "response": "Missing parameters"})
        
        player_id = parameters[0].get('id_player')
        party_id = parameters[1].get('id_party')
        if player_id not in players:
            return json.dumps({"status": "KO", "response": "Player not found"})

        return json.dumps({
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

    elif action == "gameboard_status":
        if len(parameters) < 2:
            return json.dumps({"status": "KO", "response": "Missing parameters"})
        
        # Pour l'instant, cette info est statique
        visible_cells = "010010000"
        return json.dumps({
            "status": "OK",
            "response": {
                "visible_cells": visible_cells
            }
        })

    elif action == "move":
        if len(parameters) < 3:
            return json.dumps({"status": "KO", "response": "Missing parameters"})

        # Mouvements simulés (à personnaliser plus tard)
        return json.dumps({
            "status": "OK",
            "response": {
                "round_in_progress": 1,
                "move": {
                    "next_position": {"row": 0, "col": 1}
                }
            }
        })

    return json.dumps({"status": "KO", "response": "Action non prise en charge"})

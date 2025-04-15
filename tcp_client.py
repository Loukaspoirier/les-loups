import tkinter as tk
from tkinter import messagebox
import socket
import json

# ----- Communication avec le serveur -----
def send_request(request_data):
    host = '127.0.0.1'
    port = 54320
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(json.dumps(request_data).encode('utf-8'))
        response = s.recv(4096).decode('utf-8')
        return response

# ----- Fonctions -----
def list_open_parties():
    request_data = {"action": "list", "parameters": []}
    response = send_request(request_data)
    output_text.set(response)

def subscribe():
    name = entry_player_name.get()
    try:
        party_id = int(entry_party_id.get())
    except ValueError:
        messagebox.showerror("Erreur", "L'ID de la partie doit être un nombre.")
        return
    request_data = {
        "action": "subscribe",
        "parameters": [{"player": name}, {"id_party": party_id}]
    }
    response = send_request(request_data)
    output_text.set(response)

def party_status():
    try:
        player_id = int(entry_player_id.get())
        party_id = int(entry_party_id.get())
    except ValueError:
        messagebox.showerror("Erreur", "Les IDs doivent être des nombres.")
        return
    request_data = {
        "action": "party_status",
        "parameters": [{"id_player": player_id}, {"id_party": party_id}]
    }
    response = send_request(request_data)
    output_text.set(response)

def gameboard_status():
    try:
        party_id = int(entry_party_id.get())
        player_id = int(entry_player_id.get())
    except ValueError:
        messagebox.showerror("Erreur", "Les IDs doivent être des nombres.")
        return
    request_data = {
        "action": "gameboard_status",
        "parameters": [{"id_party": party_id}, {"id_player": player_id}]
    }
    response = send_request(request_data)
    output_text.set(response)

def move():
    try:
        party_id = int(entry_party_id.get())
        player_id = int(entry_player_id.get())
        move_vector = entry_move.get()
    except ValueError:
        messagebox.showerror("Erreur", "Entrée invalide.")
        return
    request_data = {
        "action": "move",
        "parameters": [{"id_party": party_id}, {"id_player": player_id}, {"move": move_vector}]
    }
    response = send_request(request_data)
    output_text.set(response)

# ----- Interface graphique -----
root = tk.Tk()
root.title("Client Jeu Réseau")

# Champs de saisie
tk.Label(root, text="Nom du joueur:").grid(row=0, column=0, sticky="e")
entry_player_name = tk.Entry(root)
entry_player_name.grid(row=0, column=1)

tk.Label(root, text="ID de la partie:").grid(row=1, column=0, sticky="e")
entry_party_id = tk.Entry(root)
entry_party_id.grid(row=1, column=1)

tk.Label(root, text="ID du joueur:").grid(row=2, column=0, sticky="e")
entry_player_id = tk.Entry(root)
entry_player_id.grid(row=2, column=1)

tk.Label(root, text="Vecteur de déplacement (ex: 01):").grid(row=3, column=0, sticky="e")
entry_move = tk.Entry(root)
entry_move.grid(row=3, column=1)

# Boutons d'action
tk.Button(root, text="Lister les parties", command=list_open_parties).grid(row=4, column=0, pady=5)
tk.Button(root, text="S'inscrire", command=subscribe).grid(row=4, column=1)
tk.Button(root, text="Statut de la partie", command=party_status).grid(row=5, column=0)
tk.Button(root, text="État du plateau", command=gameboard_status).grid(row=5, column=1)
tk.Button(root, text="Bouger", command=move).grid(row=6, column=0, columnspan=2, pady=5)

# Zone d'affichage
output_text = tk.StringVar()
tk.Label(root, text="Réponse serveur :").grid(row=7, column=0, columnspan=2)
tk.Message(root, textvariable=output_text, width=400, bg="white", relief="sunken").grid(row=8, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

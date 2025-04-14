import tkinter as tk
from tkinter import messagebox
import socket
import json

class ClientTcpTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Client TCP - Les Loups")
        self.setup_ui()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def setup_ui(self):
        # Interface identique au client HTTP
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()
        
        self.btn_list = tk.Button(self.frame, text="Lister parties", command=self.lister_parties)
        self.btn_subscribe = tk.Button(self.frame, text="S'inscrire", command=self.inscrire)
        self.btn_move = tk.Button(self.frame, text="Déplacer", command=self.deplacer)
        
        self.btn_list.pack(pady=5)
        self.btn_subscribe.pack(pady=5)
        self.btn_move.pack(pady=5)
        
        self.text = tk.Text(self.frame, height=10, width=50)
        self.text.pack(pady=10)
        
    def envoyer_requete(self, requete):
        try:
            self.socket.connect(('localhost', 5555))
            self.socket.send(json.dumps(requete).encode())
            reponse = json.loads(self.socket.recv(1024).decode())
            self.socket.close()
            return reponse
        except Exception as e:
            return {"status": "KO", "erreur": str(e)}
    
    def lister_parties(self):
        reponse = self.envoyer_requete({
            "action": "list",
            "parameters": []
        })
        self.afficher(reponse)
    
    def inscrire(self):
        win = tk.Toplevel()
        tk.Label(win, text="ID Partie:").pack()
        id_entry = tk.Entry(win)
        id_entry.pack()
        
        tk.Label(win, text="Nom Joueur:").pack()
        nom_entry = tk.Entry(win)
        nom_entry.pack()
        
        def valider():
            reponse = self.envoyer_requete({
                "action": "subscribe",
                "parameters": [
                    {"player": nom_entry.get()},
                    {"id_party": id_entry.get()}
                ]
            })
            self.afficher(reponse)
            win.destroy()
            
        tk.Button(win, text="Valider", command=valider).pack()
    
    def deplacer(self):
        win = tk.Toplevel()
        # ... (similaire à l'inscription avec les paramètres de déplacement)
    
    def afficher(self, data):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, json.dumps(data, indent=2))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientTcpTkinter(root)
    root.mainloop()
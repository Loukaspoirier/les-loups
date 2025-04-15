import tkinter as tk
from tkinter import messagebox
import socket
import json

class ClientTcpTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Client TCP - Les Loups")
        self.setup_ui()
        self.socket = None
        self.player_id = None
        
    def setup_ui(self):
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
        
    def connect(self):
        if not self.socket:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('localhost', 5555))
        
    def envoyer_requete(self, requete):
        try:
            self.connect()
            self.socket.send(json.dumps(requete).encode())
            reponse = json.loads(self.socket.recv(2048).decode())
            return reponse
        except Exception as e:
            return {"status": "KO", "erreur": str(e)}
        finally:
            if self.socket:
                self.socket.close()
                self.socket = None
    
    def lister_parties(self):
        reponse = self.envoyer_requete({
            "action": "list",
            "parameters": []
        })
        self.afficher(reponse)
    
    def inscrire(self):
        win = tk.Toplevel(self.root)
        win.title("Inscription")
        
        tk.Label(win, text="ID Partie:").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(win)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(win, text="Nom Joueur:").grid(row=1, column=0, padx=5, pady=5)
        self.nom_entry = tk.Entry(win)
        self.nom_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(win, text="Valider", command=self.valider_inscription).grid(row=2, columnspan=2, pady=10)
        
    def valider_inscription(self):
        reponse = self.envoyer_requete({
            "action": "subscribe",
            "parameters": [
                {"player": self.nom_entry.get()},
                {"id_party": self.id_entry.get()}
            ]
        })
        if reponse.get("status") == "OK":
            self.player_id = reponse["response"].get("id_player")
        self.afficher(reponse)
        self.nom_entry.master.destroy()
    
    def deplacer(self):
        if not self.player_id:
            messagebox.showerror("Erreur", "Veuillez vous inscrire d'abord")
            return
            
        win = tk.Toplevel(self.root)
        win.title("Déplacement")
        
        tk.Label(win, text="Déplacement (ex: 0 1):").pack(pady=5)
        self.move_entry = tk.Entry(win)
        self.move_entry.pack(pady=5)
        
        tk.Button(win, text="Valider", command=self.valider_deplacement).pack(pady=10)
        
    def valider_deplacement(self):
        try:
            move = self.move_entry.get().split()
            if len(move) != 2:
                raise ValueError("Format invalide")
                
            reponse = self.envoyer_requete({
                "action": "move",
                "parameters": [
                    {"id_player": self.player_id},
                    {"move": move}
                ]
            })
            self.afficher(reponse)
            self.move_entry.master.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def afficher(self, data):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientTcpTkinter(root)
    root.mainloop()
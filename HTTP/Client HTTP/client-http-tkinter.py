import tkinter as tk
from tkinter import messagebox
from function import creer_partie_api, inscription_api, lister_parties_api, etat_partie_api, deplacer_api

class ClientTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Client HTTP - Les Loups")
        self.root.geometry("600x400")

        self.title = tk.Label(root, text="Les Loups - Interface HTTP", font=("Helvetica", 16))
        self.title.pack(pady=10)

        self.btn_creer = tk.Button(root, text="Créer une partie", command=self.creer_partie)
        self.btn_inscrire = tk.Button(root, text="S'inscrire à une partie", command=self.inscription)
        self.btn_lister = tk.Button(root, text="Lister les parties", command=self.lister_parties)
        self.btn_etat = tk.Button(root, text="Voir l'état d'une partie", command=self.etat_partie)
        self.btn_deplacer = tk.Button(root, text="Se déplacer", command=self.deplacer)
        
        self.btn_creer.pack(pady=5)
        self.btn_inscrire.pack(pady=5)
        self.btn_lister.pack(pady=5)
        self.btn_etat.pack(pady=5)
        self.btn_deplacer.pack(pady=5)

        self.output = tk.Text(root, height=10, width=70)
        self.output.pack(pady=10)

    def afficher(self, message):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, message)

    def creer_partie(self):
        win = tk.Toplevel(self.root)
        win.title("Créer une partie")

        labels = ["Lignes", "Colonnes", "Tours", "Délai (s)", "Obstacles", "Max joueurs"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries.append(entry)

        def submit():
            try:
                data = [int(e.get()) for e in entries]
                resultat = creer_partie_api(*data)
                self.afficher(str(resultat))
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(win, text="Créer", command=submit).grid(row=len(labels), columnspan=2)

    def inscription(self):
        win = tk.Toplevel(self.root)
        win.title("Inscription")

        tk.Label(win, text="ID Partie").grid(row=0, column=0)
        id_entry = tk.Entry(win)
        id_entry.grid(row=0, column=1)

        tk.Label(win, text="Nom Joueur").grid(row=1, column=0)
        nom_entry = tk.Entry(win)
        nom_entry.grid(row=1, column=1)

        def submit():
            resultat = inscription_api(id_entry.get(), nom_entry.get())
            self.afficher(str(resultat))
            win.destroy()

        tk.Button(win, text="S'inscrire", command=submit).grid(row=2, columnspan=2)

    def lister_parties(self):
        resultat = lister_parties_api()
        self.afficher(str(resultat))

    def etat_partie(self):
        win = tk.Toplevel(self.root)
        win.title("État d'une partie")

        tk.Label(win, text="ID Partie").grid(row=0, column=0)
        id_entry = tk.Entry(win)
        id_entry.grid(row=0, column=1)

        def submit():
            resultat = etat_partie_api(id_entry.get())
            self.afficher(str(resultat))
            win.destroy()

        tk.Button(win, text="Afficher", command=submit).grid(row=1, columnspan=2)

    def deplacer(self):
        win = tk.Toplevel(self.root)
        win.title("Déplacement")

        tk.Label(win, text="ID Partie").grid(row=0, column=0)
        id_partie_entry = tk.Entry(win)
        id_partie_entry.grid(row=0, column=1)

        tk.Label(win, text="ID Joueur").grid(row=1, column=0)
        id_joueur_entry = tk.Entry(win)
        id_joueur_entry.grid(row=1, column=1)

        tk.Label(win, text="Direction").grid(row=2, column=0)
        directions_frame = tk.Frame(win)  # Nom corrigé avec un "s"
        directions_frame.grid(row=2, column=1)  # Même correction ici

        # Boutons de direction
        directions = {
            "Haut": "10", "Bas": "-10",
            "Gauche": "0-1", "Droite": "01",
            "Passer": "00"
        }

        for i, (text, code) in enumerate(directions.items()):
            btn = tk.Button(directions_frame, text=text,  # Utilisation du nom corrigé
                        command=lambda c=code: self.executer_deplacement(
                            id_partie_entry.get(),
                            id_joueur_entry.get(),
                            c,
                            win
                        ))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientTkinter(root)
    root.mainloop()
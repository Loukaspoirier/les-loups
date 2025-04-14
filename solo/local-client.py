import tkinter as tk
from tkinter import ttk, messagebox
from moteur import moteur

class JeuLocal:
    def __init__(self, root):
        self.root = root
        self.root.title("Les Loups - Solo")
        self.timer_id = None
        self.setup_ui()
    
    def setup_ui(self):
        # Configuration initiale
        self.frame_config = tk.LabelFrame(self.root, text="Configuration", padx=10, pady=10)
        self.frame_config.pack(pady=5)
        
        # Paramètres de jeu
        tk.Label(self.frame_config, text="Lignes:").grid(row=0, column=0)
        self.entry_lignes = tk.Entry(self.frame_config, width=5)
        self.entry_lignes.grid(row=0, column=1)
        self.entry_lignes.insert(0, "10")
        
        tk.Label(self.frame_config, text="Colonnes:").grid(row=1, column=0)
        self.entry_colonnes = tk.Entry(self.frame_config, width=5)
        self.entry_colonnes.grid(row=1, column=1)
        self.entry_colonnes.insert(0, "10")
        
        tk.Label(self.frame_config, text="Obstacles:").grid(row=2, column=0)
        self.entry_obstacles = tk.Entry(self.frame_config, width=5)
        self.entry_obstacles.grid(row=2, column=1)
        self.entry_obstacles.insert(0, "5")
        
        tk.Label(self.frame_config, text="Tours max:").grid(row=3, column=0)
        self.entry_tours = tk.Entry(self.frame_config, width=5)
        self.entry_tours.grid(row=3, column=1)
        self.entry_tours.insert(0, "20")
        
        tk.Label(self.frame_config, text="Durée tour (s):").grid(row=4, column=0)
        self.entry_duree = tk.Entry(self.frame_config, width=5)
        self.entry_duree.grid(row=4, column=1)
        self.entry_duree.insert(0, "30")
        
        self.role_var = tk.StringVar(value="loup")
        tk.Radiobutton(self.frame_config, text="Jouer Loup", variable=self.role_var, value="loup").grid(row=5, column=0)
        tk.Radiobutton(self.frame_config, text="Jouer Villageois", variable=self.role_var, value="villageois").grid(row=5, column=1)
        
        tk.Button(self.frame_config, text="Démarrer", command=self.demarrer_partie).grid(row=6, columnspan=2, pady=5)
        
        # Éléments de jeu (initialement cachés)
        self.frame_jeu = tk.LabelFrame(self.root, text="Plateau de jeu", padx=5, pady=5)
        self.canvas = tk.Canvas(self.frame_jeu, width=500, height=500, bg='white')
        self.canvas.pack()
        
        self.frame_controles = tk.Frame(self.root)
        self.btn_directions = []
        
        self.frame_info = tk.LabelFrame(self.root, text="Informations", padx=5, pady=5)
        self.label_tour = tk.Label(self.frame_info, text="Tour: 0/0")
        self.label_tour.pack()
        self.label_temps = tk.Label(self.frame_info, text="Temps restant: 0s")
        self.label_temps.pack()
        self.label_statut = tk.Label(self.frame_info, text="En attente...")
        self.label_statut.pack()
        
        self.progress = ttk.Progressbar(self.frame_info, orient='horizontal', length=200, mode='determinate')
        self.progress.pack(pady=5)
    
    def demarrer_partie(self):
        try:
            nb_lignes = int(self.entry_lignes.get())
            nb_colonnes = int(self.entry_colonnes.get())
            nb_obstacles = int(self.entry_obstacles.get())
            
            # Validation des obstacles
            max_obstacles = (nb_lignes * nb_colonnes) - 2
            if nb_obstacles > max_obstacles:
                messagebox.showerror("Erreur", f"Maximum {max_obstacles} obstacles pour cette taille")
                return
                
            config = {
                'nb_lignes': nb_lignes,
                'nb_colonnes': nb_colonnes,
                'nb_obstacles': nb_obstacles,
                'nb_tours': int(self.entry_tours.get()),
                'duree_tour': int(self.entry_duree.get()),
                'role_joueur': self.role_var.get()
            }
            
            if not moteur.creer_partie(config):
                messagebox.showerror("Erreur", "Configuration invalide - Impossible de placer les obstacles")
                return
            
            self.frame_config.pack_forget()
            self.frame_jeu.pack(pady=5)
            self.frame_info.pack(pady=5)
            self._setup_controles()
            self.dessiner_plateau()
            self.commencer_tour(config['duree_tour'])
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")
    
    def _setup_controles(self):
        for btn in self.btn_directions:
            btn.destroy()
        
        self.btn_directions = []
        directions = ['haut', 'bas', 'gauche', 'droite']
        
        for i, dir in enumerate(directions):
            btn = tk.Button(
                self.frame_controles, 
                text=dir.capitalize(), 
                width=8,
                command=lambda d=dir: self.deplacer(d)
            )
            btn.grid(row=0, column=i, padx=2)
            self.btn_directions.append(btn)
        
        self.frame_controles.pack(pady=5)
    
    def commencer_tour(self, duree):
        if not moteur.commencer_tour(duree):
            messagebox.showinfo("Fin", "Nombre maximum de tours atteint!")
            self.root.quit()
            return
        
        self.progress['maximum'] = duree
        self.progress['value'] = duree
        self._update_ui_tour()
        self._start_timer(duree)
    
    def _start_timer(self, duree):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.timer_id = self.root.after(1000, self._update_timer, duree-1)
    
    def _update_timer(self, temps_restant):
        if temps_restant <= 0:
            self.timer_id = None
            self.label_statut.config(text="Temps écoulé!")
            self.progress['value'] = 0
            return
        
        self.progress['value'] = temps_restant
        self.label_temps.config(text=f"Temps restant: {temps_restant}s")
        self.timer_id = self.root.after(1000, self._update_timer, temps_restant-1)
    
    def _update_ui_tour(self):
        config = moteur.partie['config']
        self.label_tour.config(
            text=f"Tour: {moteur.partie['tour_actuel']}/{config['nb_tours']}"
        )
        self.label_temps.config(
            text=f"Temps restant: {config['duree_tour']}s"
        )
        self.label_statut.config(text="Tour en cours...")
    
    def dessiner_plateau(self):
        self.canvas.delete("all")
        if not moteur.partie:
            return
        
        config = moteur.partie['config']
        cell_w = 500 // config['nb_colonnes']
        cell_h = 500 // config['nb_lignes']
        
        # Récupérer les cases visibles
        plateau_visible = moteur.get_plateau_visible(moteur.partie['joueur']['position'])
        
        for i in range(config['nb_lignes']):
            for j in range(config['nb_colonnes']):
                if plateau_visible[i][j] is not None:
                    color = 'white'
                    if plateau_visible[i][j] == 'obstacle':
                        color = 'gray'
                    elif plateau_visible[i][j] in ['loup', 'villageois']:
                        # Dessiner le NPC
                        self.canvas.create_rectangle(
                            j * cell_w + 5, i * cell_h + 5,
                            (j+1) * cell_w - 5, (i+1) * cell_h - 5,
                            fill="red" if plateau_visible[i][j] == 'loup' else "blue"
                        )
                    
                    self.canvas.create_rectangle(
                        j * cell_w, i * cell_h,
                        (j+1) * cell_w, (i+1) * cell_h,
                        fill=color, outline="lightgray"
                    )
        
        # Dessiner le joueur
        j_pos = moteur.partie['joueur']['position']
        self.canvas.create_oval(
            j_pos[1] * cell_w + 5, j_pos[0] * cell_h + 5,
            (j_pos[1]+1) * cell_w - 5, (j_pos[0]+1) * cell_h - 5,
            fill="red" if moteur.partie['joueur']['role'] == 'loup' else "blue"
        )
    
    def deplacer(self, direction):
        result = moteur.deplacer_joueur(direction)
        
        if result['statut'] == 'fin':
            messagebox.showinfo("Fin de partie", result['message'])
            self.root.quit()
            return
        
        self.label_statut.config(text=result['message'])
        self.dessiner_plateau()
        
        if not moteur.partie['termine']:
            self.commencer_tour(moteur.partie['config']['duree_tour'])

if __name__ == "__main__":
    root = tk.Tk()
    jeu = JeuLocal(root)
    root.mainloop()
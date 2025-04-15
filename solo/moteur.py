import random
from collections import deque

class MoteurJeuLocal:
    def __init__(self):
        self.partie = None
        self.tour_en_cours = False
        self.temps_restant = 0
    
    def creer_partie(self, config):
        """Crée une partie avec configuration et retourne True si réussie"""
        self.partie = {
            'config': config,
            'plateau': self._init_plateau(config),
            'joueur': {
                'role': config['role_joueur'],
                'position': [0, 0]  # Position de départ en haut à gauche
            },
            'npc': {
                'role': 'loup' if config['role_joueur'] == 'villageois' else 'villageois',
                'position': [config['nb_lignes']-1, config['nb_colonnes']-1]  # Coin opposé
            },
            'tour_actuel': 0,
            'termine': False
        }
        return self._placer_obstacles(config['nb_obstacles'])
    
    def _init_plateau(self, config):
        return [[None for _ in range(config['nb_colonnes'])] 
                for _ in range(config['nb_lignes'])]
    
    def _placer_obstacles(self, nb_obstacles):
        """Place les obstacles en garantissant un chemin valide"""
        positions_interdites = [
            self.partie['joueur']['position'],
            self.partie['npc']['position']
        ]
        
        def chemin_possible():
            directions = [(0,1), (1,0), (0,-1), (-1,0)]
            visite = set()
            file = deque([tuple(self.partie['joueur']['position'])])
            
            while file:
                x, y = file.popleft()
                if [x,y] == self.partie['npc']['position']:
                    return True
                
                for dx, dy in directions:
                    nx, ny = x+dx, y+dy
                    if (0 <= nx < len(self.partie['plateau'])) and \
                       (0 <= ny < len(self.partie['plateau'][0])) and \
                       (nx, ny) not in visite and \
                       self.partie['plateau'][nx][ny] != 'obstacle':
                        visite.add((nx, ny))
                        file.append((nx, ny))
            return False
        
        obstacles_places = 0
        tentatives = 0
        max_tentatives = 100
        
        while obstacles_places < nb_obstacles and tentatives < max_tentatives:
            tentatives += 1
            x, y = random.randint(0, len(self.partie['plateau'])-1), \
                   random.randint(0, len(self.partie['plateau'][0])-1)
            
            if [x,y] not in positions_interdites and self.partie['plateau'][x][y] is None:
                self.partie['plateau'][x][y] = 'obstacle'
                if chemin_possible():
                    obstacles_places += 1
                else:
                    self.partie['plateau'][x][y] = None
        
        return obstacles_places == nb_obstacles
    
    def commencer_tour(self, duree_tour):
        if self.partie['tour_actuel'] >= self.partie['config']['nb_tours']:
            return False
        
        self.tour_en_cours = True
        self.temps_restant = duree_tour
        self.partie['tour_actuel'] += 1
        return True
    
    def get_plateau_visible(self, position_joueur, portee=1):
        """Retourne seulement les cases visibles autour du joueur"""
        visible = [[None for _ in range(len(self.partie['plateau'][0]))] 
                  for _ in range(len(self.partie['plateau']))]
        
        x, y = position_joueur
        for i in range(max(0, x-portee), min(len(self.partie['plateau']), x+portee+1)):
            for j in range(max(0, y-portee), min(len(self.partie['plateau'][0]), y+portee+1)):
                visible[i][j] = self.partie['plateau'][i][j]
                if [i,j] == self.partie['npc']['position']:
                    visible[i][j] = self.partie['npc']['role']
        return visible
    
    def deplacer_joueur(self, direction):
        """Gère le déplacement et consomme toujours un tour"""
        if not self.tour_en_cours or self.partie['termine']:
            return {'statut': 'erreur', 'message': 'Tour non actif'}
        
        self.tour_en_cours = False
        dir_map = {
            'haut': (-1, 0), 'bas': (1, 0),
            'gauche': (0, -1), 'droite': (0, 1)
        }
        
        dx, dy = dir_map.get(direction, (0, 0))
        x, y = self.partie['joueur']['position']
        new_x, new_y = x + dx, y + dy
        
        if (0 <= new_x < len(self.partie['plateau'])) and \
           (0 <= new_y < len(self.partie['plateau'][0])) and \
           (self.partie['plateau'][new_x][new_y] != 'obstacle'):
            
            self.partie['joueur']['position'] = [new_x, new_y]
            resultat = self._check_rencontre()
            if resultat:
                return resultat
            return {'statut': 'deplacement', 'message': 'Déplacement réussi'}
        
        return {'statut': 'obstacle', 'message': 'Déplacement bloqué'}
    
    def _check_rencontre(self):
        if self.partie['joueur']['position'] == self.partie['npc']['position']:
            self.partie['termine'] = True
            victoire = self.partie['joueur']['role'] == 'loup'
            return {
                'statut': 'fin',
                'message': 'Victoire!' if victoire else 'Défaite!',
                'gagnant': 'joueur' if victoire else 'npc'
            }
        return None

moteur = MoteurJeuLocal()
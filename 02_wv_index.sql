ALTER TABLE parties DROP COLUMN id_party;
ALTER TABLE parties ADD COLUMN id_party SERIAL PRIMARY KEY;
ALTER TABLE parties ADD nb_turns INT;
ALTER TABLE parties ADD turn_duration INTERVAL;

ALTER TABLE roles DROP COLUMN IF EXISTS id_role;
ALTER TABLE roles ADD COLUMN id_role SERIAL PRIMARY KEY;


ALTER TABLE players DROP COLUMN IF EXISTS id_player;
ALTER TABLE players ADD COLUMN id_player SERIAL PRIMARY KEY;

-- Ajouter les clés étrangères dans la table roles_quotas
ALTER TABLE roles_quotas
ADD CONSTRAINT fk_roles_quotas_party FOREIGN KEY (id_party) REFERENCES parties(id_party),
ADD CONSTRAINT fk_roles_quotas_role FOREIGN KEY (id_role) REFERENCES roles(id_role);

-- Ajouter les clés étrangères dans la table obstacles
ALTER TABLE obstacles DROP COLUMN IF EXISTS id_obstacle;
ALTER TABLE obstacles ADD COLUMN id_obstacle SERIAL PRIMARY KEY;
ALTER TABLE obstacles ADD CONSTRAINT fk_obstacles_party FOREIGN KEY (id_party) REFERENCES parties(id_party);

-- Ajouter les clés étrangères dans la table players_in_parties

ALTER TABLE players_in_parties DROP COLUMN IF EXISTS id_players_in_parties;
ALTER TABLE players_in_parties ADD COLUMN id_players_in_parties SERIAL PRIMARY KEY;
ALTER TABLE players_in_parties
ADD CONSTRAINT fk_players_in_parties_party FOREIGN KEY (id_party) REFERENCES parties(id_party),
ADD CONSTRAINT fk_players_in_parties_player FOREIGN KEY (id_player) REFERENCES players(id_player),
ADD CONSTRAINT fk_players_in_parties_role FOREIGN KEY (id_role) REFERENCES roles(id_role);

-- Ajouter les clés étrangères dans la table turns

ALTER TABLE turns DROP COLUMN IF EXISTS id_turn;
ALTER TABLE turns ADD COLUMN id_turn SERIAL PRIMARY KEY;
ALTER TABLE turns
ADD CONSTRAINT fk_turns_party FOREIGN KEY (id_party) REFERENCES parties(id_party);

-- Ajouter les clés étrangères dans la table players_play
ALTER TABLE players_play
ADD CONSTRAINT fk_players_play_in_parties FOREIGN KEY (id_players_in_parties) REFERENCES players_in_parties(id_players_in_parties),
ADD CONSTRAINT fk_players_play_turn FOREIGN KEY (id_turn) REFERENCES turns(id_turn);
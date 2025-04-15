CREATE TABLE parties (
    id_party int,
    title_party text
);

create table roles_quotas (
    id_party int,
    id_role int,
    min_quota int,
    max_quota text
);

create table obstacles (
    id_party int,
    id_obstacle int,
    position_col text,
    position_row text
);

create table roles (
    id_role int,
    description_role text
);

create table players (
    id_player int,
    pseudo text
);

create table players_in_parties (
    id_players_in_parties int,
    id_party int,
    id_player int,
    id_role int,
    is_alive text
);

create table turns (
    id_turn int,
    id_party int,
    start_time timestamp,
    end_time timestamp
);

create table players_play (
    id_players_in_parties int,
    id_turn int,
    start_time timestamp,
    end_time timestamp,
    action varchar(10),
    origin_position_col text,
    origin_position_row text,
    target_position_col text,
    target_position_row text
);





ALTER TABLE parties
ADD PRIMARY KEY (id_party);

ALTER TABLE roles
ADD PRIMARY KEY (id_role);

ALTER TABLE players
ADD PRIMARY KEY (id_player);

-- Ajouter les clés étrangères dans la table roles_quotas
ALTER TABLE roles_quotas
ADD CONSTRAINT fk_roles_quotas_party FOREIGN KEY (id_party) REFERENCES parties(id_party),
ADD CONSTRAINT fk_roles_quotas_role FOREIGN KEY (id_role) REFERENCES roles(id_role);

-- Ajouter les clés étrangères dans la table obstacles
ALTER TABLE obstacles
ADD PRIMARY KEY (id_obstacle);
ADD CONSTRAINT fk_obstacles_party FOREIGN KEY (id_party) REFERENCES parties(id_party),

-- Ajouter les clés étrangères dans la table players_in_parties
ALTER TABLE players_in_parties
ADD PRIMARY KEY (id_players_in_parties);
ADD CONSTRAINT fk_players_in_parties_party FOREIGN KEY (id_party) REFERENCES parties(id_party),
ADD CONSTRAINT fk_players_in_parties_player FOREIGN KEY (id_player) REFERENCES players(id_player),
ADD CONSTRAINT fk_players_in_parties_role FOREIGN KEY (id_role) REFERENCES roles(id_role);

-- Ajouter les clés étrangères dans la table turns
ALTER TABLE turns
ADD PRIMARY KEY (id_turn);
ADD CONSTRAINT fk_turns_party FOREIGN KEY (id_party) REFERENCES parties(id_party);

-- Ajouter les clés étrangères dans la table players_play
ALTER TABLE players_play
ADD CONSTRAINT fk_players_play_in_parties FOREIGN KEY (id_players_in_parties) REFERENCES players_in_parties(id_players_in_parties),
ADD CONSTRAINT fk_players_play_turn FOREIGN KEY (id_turn) REFERENCES turns(id_turn);

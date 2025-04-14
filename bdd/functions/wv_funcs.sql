DELIMITER $$

CREATE FUNCTION random_position(party_id INT) 
RETURNS POINT
DETERMINISTIC
BEGIN
    DECLARE pos POINT;
    DECLARE max_x INT;
    DECLARE max_y INT;

    -- Détermine les dimensions de la grille de la partie
    SELECT max_x, max_y INTO max_x, max_y
    FROM parties
    WHERE id_party = party_id;

    -- Génère une position aléatoire qui n'a pas encore été choisie
    LOOP
        SET pos = POINT(RAND() * max_x, RAND() * max_y);
        -- Vérifie que la position n'a pas déjà été choisie
        IF NOT EXISTS (
            SELECT 1 FROM players_in_parties pip
            WHERE pip.id_party = party_id AND ST_Equals(pip.position, pos)
        ) THEN
            RETURN pos;
        END IF;
    END LOOP;

END$$

DELIMITER ;

DELIMITER $$

CREATE FUNCTION random_role(party_id INT) 
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE role_count INT;
    DECLARE role VARCHAR(20);
    DECLARE wolf_quota INT;
    DECLARE villager_quota INT;

    -- Récupère les quotas de loups et de villageois pour la partie
    SELECT loup_quota, villageois_quota INTO wolf_quota, villager_quota
    FROM parties
    WHERE id_party = party_id;

    -- Compte le nombre de loups et de villageois déjà affectés
    SELECT COUNT(*) INTO role_count
    FROM players_in_parties pip
    JOIN roles r ON pip.id_role = r.id_role
    WHERE pip.id_party = party_id AND r.nom = 'loup';

    IF role_count < wolf_quota THEN
        SET role = 'loup';
    ELSE
        SET role = 'villageois';
    END IF;

    RETURN role;
END$$

DELIMITER ;
DELIMITER $$

CREATE FUNCTION get_the_winner(party_id INT)
RETURNS TABLE (
    nom_joueur VARCHAR(255),
    role VARCHAR(20),
    nom_partie VARCHAR(255),
    nb_tours_joues INT,
    nb_total_tours INT,
    temps_moyen_prise_decision FLOAT
)
DETERMINISTIC
BEGIN
    DECLARE winner_id INT;
    DECLARE winner_role VARCHAR(20);
    DECLARE nb_total_tours INT;

    -- Récupère l'id du vainqueur et son rôle
    SELECT id_player, role.nom
    INTO winner_id, winner_role
    FROM parties pa
    JOIN players_in_parties pip ON pa.id_party = pip.id_party
    JOIN roles role ON pip.id_role = role.id_role
    WHERE pa.id_party = party_id AND pa.vainqueur = pip.id_player;

    -- Récupère le nombre total de tours de la partie
    SELECT COUNT(*) INTO nb_total_tours
    FROM turns t
    WHERE t.id_party = party_id;

    -- Récupère les statistiques du vainqueur
    RETURN QUERY
    SELECT
        p.nom AS nom_joueur,
        winner_role AS role,
        pa.nom AS nom_partie,
        (SELECT COUNT(*) FROM turns t JOIN players_in_parties pip ON t.id_party = pip.id_party WHERE pip.id_player = winner_id) AS nb_tours_joues,
        nb_total_tours,
        (SELECT AVG(TIMESTAMPDIFF(SECOND, t.date_heure, dp.date_heure)) FROM turns t JOIN decision_points dp ON t.id_turn = dp.id_turn WHERE dp.id_player = winner_id) AS temps_moyen_prise_decision
    FROM
        players p
    JOIN parties pa ON p.id_player = winner_id
    WHERE pa.id_party = party_id;
END$$

DELIMITER ;

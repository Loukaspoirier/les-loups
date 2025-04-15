-- Fonction 1 : Génération d'une position aléatoire
CREATE OR REPLACE FUNCTION random_position(party_id INT, max_x INT, max_y INT)
RETURNS TABLE (position_col TEXT, position_row TEXT) AS $$
DECLARE
    try_col TEXT;
    try_row TEXT;
    tries INT := 0;
BEGIN
    LOOP
        try_col := FLOOR(random() * max_x)::INT::TEXT;
        try_row := FLOOR(random() * max_y)::INT::TEXT;

        IF NOT EXISTS (
            SELECT 1
            FROM players_in_parties
            WHERE id_party = party_id
              AND position_col = try_col
              AND position_row = try_row
        ) THEN
            RETURN QUERY SELECT try_col, try_row;
            EXIT;
        END IF;

        tries := tries + 1;
        IF tries > 100 THEN
            RAISE EXCEPTION 'Trop de tentatives de génération de position unique';
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Fonction 2 : Attribution d'un rôle aléatoire selon les quotas
CREATE OR REPLACE FUNCTION random_role(party_id INT)
RETURNS TEXT AS $$
DECLARE
    wolf_quota INT;
    villager_quota INT;
    wolf_count INT;
    selected_role TEXT;
BEGIN
    SELECT min_quota::INT INTO wolf_quota
    FROM roles_quotas rq
    JOIN roles r ON rq.id_role = r.id_role
    WHERE id_party = party_id AND r.description_role = 'loup';

    SELECT COUNT(*) INTO wolf_count
    FROM players_in_parties pip
    JOIN roles r ON pip.id_role = r.id_role
    WHERE pip.id_party = party_id AND r.description_role = 'loup';

    IF wolf_count < wolf_quota THEN
        selected_role := 'loup';
    ELSE
        selected_role := 'villageois';
    END IF;

    RETURN selected_role;
END;
$$ LANGUAGE plpgsql;


-- Fonction 3 : Résumé du vainqueur d'une partie
CREATE OR REPLACE FUNCTION get_the_winner(party_id INT)
RETURNS TABLE (
    nom_joueur TEXT,
    role TEXT,
    nom_partie TEXT,
    nb_tours_joues INT,
    nb_total_tours INT,
    temps_moyen_prise_decision DOUBLE PRECISION
) AS $$
DECLARE
    winner_id INT;
    winner_role TEXT;
    total_turns INT;
BEGIN
    -- ID et rôle du vainqueur
    SELECT pip.id_player, r.description_role
    INTO winner_id, winner_role
    FROM parties pa
    JOIN players_in_parties pip ON pa.id_party = pip.id_party
    JOIN roles r ON pip.id_role = r.id_role
    WHERE pa.id_party = party_id AND pa.vainqueur = pip.id_player;

    -- Nombre total de tours de la partie
    SELECT COUNT(*) INTO total_turns
    FROM turns
    WHERE id_party = party_id;

    -- Retourne les données du gagnant
    RETURN QUERY
    SELECT
        p.pseudo,
        winner_role,
        pa.title_party,
        (
            SELECT COUNT(*)
            FROM turns t
            JOIN players_play pp ON pp.id_turn = t.id_turn
            JOIN players_in_parties pip ON pip.id_players_in_parties = pp.id_players_in_parties
            WHERE t.id_party = party_id AND pip.id_player = winner_id
        ) AS nb_tours_joues,
        total_turns,
        (
            SELECT AVG(EXTRACT(EPOCH FROM (pp.end_time - pp.start_time)))
            FROM players_play pp
            JOIN players_in_parties pip ON pip.id_players_in_parties = pp.id_players_in_parties
            WHERE pip.id_player = winner_id
        ) AS temps_moyen_prise_decision
    FROM players p
    JOIN parties pa ON p.id_player = winner_id
    WHERE pa.id_party = party_id;
END;
$$ LANGUAGE plpgsql;

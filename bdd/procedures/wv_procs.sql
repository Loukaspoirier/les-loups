CREATE OR REPLACE FUNCTION seed_data(nb_players INT, party_id INT)
RETURNS VOID AS $$
DECLARE
    total_turns INT;
    i INT := 1;
BEGIN
    total_turns := nb_players * 2;

    WHILE i <= total_turns LOOP
        INSERT INTO turns (id_party, numero, date_heure)
        VALUES (party_id, i, NOW());
        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION complete_tour(tour_id INT, party_id INT)
RETURNS VOID AS $$
DECLARE
    conflict INT;
BEGIN
    -- Appliquer les déplacements
    UPDATE players_in_parties pip
    SET position = pm.new_position
    FROM player_moves pm
    WHERE pip.id_player = pm.id_player
    AND pm.id_turn = tour_id;

    -- Vérification des conflits
    SELECT COUNT(*) INTO conflict
    FROM players_in_parties pip1
    JOIN players_in_parties pip2
        ON pip1.position = pip2.position
    WHERE pip1.id_party = party_id
      AND pip2.id_party = party_id
      AND pip1.id_player <> pip2.id_player;

    -- Résolution des conflits
    IF conflict > 0 THEN
        UPDATE players_in_parties
        SET position = 'default_position'
        WHERE id_party = party_id;
    END IF;

    -- Finaliser le tour
    UPDATE turns
    SET statut = 'completed',
        date_heure = NOW()
    WHERE id_turn = tour_id AND id_party = party_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION username_to_lower()
RETURNS VOID AS $$
BEGIN
    UPDATE players
    SET nom = LOWER(nom);
END;
$$ LANGUAGE plpgsql;


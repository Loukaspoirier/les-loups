DELIMITER $$

CREATE PROCEDURE SEED_DATA(NB_PLAYERS INT, PARTY_ID INT)
BEGIN
    DECLARE total_turns INT;
    DECLARE i INT DEFAULT 1;

    -- Calculer le nombre de tours à créer en fonction du nombre de joueurs
    SET total_turns = NB_PLAYERS * 2;  -- Par exemple, chaque joueur peut jouer 2 tours

    -- Créer les tours pour la partie donnée
    WHILE i <= total_turns DO
        INSERT INTO turns (id_party, numero, date_heure)
        VALUES (PARTY_ID, i, NOW());  -- Insérer le tour avec l'ID de la partie et la date actuelle
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE COMPLETE_TOUR(TOUR_ID INT, PARTY_ID INT)
BEGIN
    DECLARE conflict INT;

    -- Appliquer toutes les demandes de déplacement pour ce tour
    -- La logique ci-dessous vérifie les conflits avant d'appliquer un déplacement
    -- Pour cet exemple, un conflit est défini comme deux joueurs demandant de se déplacer vers la même position.

    -- Résolution des conflits de déplacement
    UPDATE players_in_parties pip
    JOIN player_moves pm ON pip.id_player = pm.id_player
    SET pip.position = pm.new_position
    WHERE pm.id_turn = TOUR_ID;

    -- Vérification des conflits : deux joueurs sur la même position
    SET conflict = (SELECT COUNT(*)
                    FROM players_in_parties pip1
                    JOIN players_in_parties pip2
                    ON pip1.position = pip2.position
                    WHERE pip1.id_party = PARTY_ID
                    AND pip1.id_player != pip2.id_player);
    
    IF conflict > 0 THEN
        -- Si des conflits sont détectés, résolvez-les (par exemple, assigner une position par défaut ou relancer)
        -- Ici, on peut choisir de faire revenir tous les joueurs à leur position initiale ou utiliser une autre logique
        UPDATE players_in_parties 
        SET position = 'default_position'
        WHERE id_party = PARTY_ID;
    END IF;
    
    -- Finaliser les déplacements et clore le tour
    UPDATE turns
    SET statut = 'completed', date_heure = NOW()
    WHERE id_turn = TOUR_ID AND id_party = PARTY_ID;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE USERNAME_TO_LOWER()
BEGIN
    -- Met à jour tous les noms dans la table players pour les convertir en minuscules
    UPDATE players
    SET nom = LOWER(nom);
END$$

DELIMITER ;

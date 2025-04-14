DELIMITER $$

CREATE TRIGGER after_tour_completed
AFTER UPDATE ON turns
FOR EACH ROW
BEGIN
    -- Vérifie si le statut du tour a été mis à "completed"
    IF NEW.statut = 'completed' AND OLD.statut != 'completed' THEN
        -- Appel de la procédure COMPLETE_TOUR pour appliquer les demandes de déplacement et résoudre les conflits
        CALL COMPLETE_TOUR(NEW.id_turn, NEW.id_party);
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER after_player_signup
AFTER INSERT ON players
FOR EACH ROW
BEGIN
    -- Appel de la procédure USERNAME_TO_LOWER pour mettre le nom du joueur en minuscules
    CALL USERNAME_TO_LOWER();
END$$

DELIMITER ;
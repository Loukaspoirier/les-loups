CREATE OR REPLACE FUNCTION after_tour_completed()
RETURNS trigger AS $$
BEGIN
    IF NEW.statut = 'completed' AND OLD.statut IS DISTINCT FROM 'completed' THEN
        PERFORM complete_tour(NEW.id_turn, NEW.id_party);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_tour_completed
AFTER UPDATE ON turns
FOR EACH ROW
EXECUTE FUNCTION after_tour_completed();


CREATE OR REPLACE FUNCTION trg_after_player_signup()
RETURNS trigger AS $$
BEGIN
    PERFORM username_to_lower();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_player_signup
AFTER INSERT ON players
FOR EACH ROW
EXECUTE FUNCTION trg_after_player_signup();

-- Vues simples

CREATE VIEW v_obstacles AS
SELECT * FROM obstacles;

CREATE VIEW v_parties AS
SELECT * FROM parties;

CREATE VIEW v_players_in_parties AS
SELECT * FROM players_in_parties;

CREATE VIEW v_players_play AS
SELECT * FROM players_play;

CREATE VIEW v_players AS
SELECT * FROM players;

CREATE VIEW v_roles_quotas AS
SELECT * FROM roles_quotas;

CREATE VIEW v_roles AS
SELECT * FROM roles;

CREATE VIEW v_turns AS
SELECT * FROM turns;


-- Vue : temps total par joueur et partie

CREATE VIEW ALL_PLAYERS_ELAPSED_GAME AS
SELECT
    p.pseudo AS nom_joueur,
    pa.title_party AS nom_partie,
    COUNT(DISTINCT pip.id_player) AS nombre_participants,
    MIN(t.start_time) AS date_premiere_action,
    MAX(t.end_time) AS date_derniere_action,
    EXTRACT(EPOCH FROM MAX(t.end_time) - MIN(t.start_time))::INT AS nb_secondes_passées
FROM
    players p
JOIN
    players_in_parties pip ON p.id_player = pip.id_player
JOIN
    parties pa ON pip.id_party = pa.id_party
JOIN
    turns t ON pip.id_party = t.id_party
GROUP BY
    p.pseudo, pa.title_party
ORDER BY
    pa.title_party ASC, p.pseudo ASC;



-- Vue : temps passé par tour

CREATE VIEW ALL_PLAYERS_ELAPSED_TOUR AS
SELECT
    p.pseudo AS nom_joueur,
    pa.title_party AS nom_partie,
    pa.nb_turns AS numero_tour, -- Si `numero` n'existe pas, remplace ou ajoute-le dans `turns`
    t.start_time AS debut_tour,
    dp.date_decision AS prise_decision,
    EXTRACT(EPOCH FROM dp.date_decision - t.start_time)::INT AS secondes_passées_dans_tour
FROM
    players p
JOIN
    players_in_parties pip ON p.id_player = pip.id_player
JOIN
    parties pa ON pip.id_party = pa.id_party
JOIN
    turns t ON pip.id_party = t.id_party
JOIN
    decision_points dp ON t.id_turn = dp.id_turn AND dp.id_player = p.id_player
ORDER BY
    pa.title_party ASC, p.pseudo ASC, pa.nb_turns ASC;



-- Vue : statistiques par joueur/partie

CREATE VIEW ALL_PLAYERS_STATS AS
WITH total_turns_per_party AS (
    SELECT id_party, COUNT(*) AS nb_total_tours
    FROM turns
    GROUP BY id_party
)
SELECT
    p.pseudo AS nom_joueur,
    r.description_role AS role,
    pa.title_party AS nom_partie,
    COUNT(DISTINCT t.id_turn) AS nb_tours_joues,
    tt.nb_total_tours,
    NULL AS vainqueur, -- À adapter selon ta logique métier
    NULL AS temps_moyen_prise_decision -- À adapter quand tu auras les données
FROM
    players p
JOIN
    players_in_parties pip ON p.id_player = pip.id_player
JOIN
    parties pa ON pip.id_party = pa.id_party
JOIN
    roles r ON pip.id_role = r.id_role
JOIN
    turns t ON pip.id_party = t.id_party
JOIN
    total_turns_per_party tt ON pa.id_party = tt.id_party
GROUP BY
    p.pseudo, r.description_role, pa.title_party, tt.nb_total_tours
ORDER BY
    pa.title_party ASC, p.pseudo ASC;



-- Vue : stats globales d’un joueur

CREATE VIEW ALL_PLAYERS AS
SELECT
    p.pseudo AS nom_joueur,
    COUNT(DISTINCT pip.id_party) AS nombre_parties_jouees,
    COUNT(t.id_turn) AS nombre_tours_joues,
    MIN(t.start_time) AS date_premiere_participation,
    MAX(t.end_time) AS date_derniere_action
FROM
    players p
JOIN
    players_in_parties pip ON p.id_player = pip.id_player
JOIN
    turns t ON pip.id_party = t.id_party
GROUP BY
    p.pseudo
ORDER BY
    nombre_parties_jouees DESC,
    date_premiere_participation ASC,
    date_derniere_action DESC,
    p.pseudo ASC;

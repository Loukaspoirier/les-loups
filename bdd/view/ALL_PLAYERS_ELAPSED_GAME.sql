CREATE VIEW ALL_PLAYERS_ELAPSED_GAME AS
SELECT
    p.nom AS nom_joueur,
    pa.nom AS nom_partie,
    COUNT(DISTINCT pip.id_player) AS nombre_participants,
    MIN(t.date_heure) AS date_premiere_action,
    MAX(t.date_heure) AS date_derniere_action,
    TIMESTAMPDIFF(SECOND, MIN(t.date_heure), MAX(t.date_heure)) AS nb_secondes_passées
FROM
    players p
JOIN
    players_in_parties pip ON p.id_player = pip.id_player
JOIN
    parties pa ON pip.id_party = pa.id_party
JOIN
    turns t ON pip.id_party = t.id_party
GROUP BY
    p.id_player, pa.id_party
ORDER BY
    pa.nom ASC, p.nom ASC;
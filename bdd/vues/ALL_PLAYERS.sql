CREATE VIEW ALL_PLAYERS AS
SELECT
    p.nom AS nom_joueur,
    COUNT(DISTINCT pip.id_party) AS nombre_parties_jouees,
    COUNT(t.id_turn) AS nombre_tours_joues,
    MIN(t.date_heure) AS date_premiere_participation,
    MAX(t.date_heure) AS date_derniere_action
FROM
    players p
JOIN
    players_in_parties pip ON p.id_player = pip.id_player
JOIN
    turns t ON pip.id_party = t.id_party
GROUP BY
    p.id_player, p.nom
ORDER BY
    nombre_parties_jouees DESC,
    date_premiere_participation ASC,
    date_derniere_action DESC,
    p.nom ASC;
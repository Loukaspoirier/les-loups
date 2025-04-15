CREATE VIEW ALL_PLAYERS_STATS AS
SELECT
    p.nom AS nom_joueur,
    r.nom AS role,
    pa.nom AS nom_partie,
    COUNT(DISTINCT t.id_turn) AS nb_tours_joues,
    (SELECT COUNT(*) FROM turns WHERE id_party = pa.id_party) AS nb_total_tours,
    CASE 
        WHEN r.nom = 'loup' AND pa.vainqueur = 'loup' THEN 'Gagnant'
        WHEN r.nom = 'villageois' AND pa.vainqueur = 'villageois' THEN 'Gagnant'
        ELSE 'Perdant'
    END AS vainqueur,
    AVG(TIMESTAMPDIFF(SECOND, t.date_heure, dp.date_heure)) AS temps_moyen_prise_decision
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
    decision_points dp ON t.id_turn = dp.id_turn AND dp.id_player = p.id_player
GROUP BY
    p.id_player, r.id_role, pa.id_party
ORDER BY
    pa.nom ASC, p.nom ASC;

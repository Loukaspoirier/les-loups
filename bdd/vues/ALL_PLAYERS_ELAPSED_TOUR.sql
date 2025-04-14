CREATE VIEW ALL_PLAYERS_ELAPSED_TOUR AS
SELECT
    p.nom AS nom_joueur,
    pa.nom AS nom_partie,
    t.numero AS numero_tour,
    t.date_heure AS debut_tour,
    dp.date_heure AS prise_decision,
    TIMESTAMPDIFF(SECOND, t.date_heure, dp.date_heure) AS secondes_passées_dans_tour
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
    pa.nom ASC, p.nom ASC, t.numero ASC;

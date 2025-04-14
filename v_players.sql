CREATE VIEW ALL_PLAYERS AS
SELECT 
    p.pseudo AS nom_joueur,
    COUNT(DISTINCT pp.id_party) AS nombre_de_parties,
    COUNT(DISTINCT pl.id_players_in_parties) AS nombre_de_tours_joues,
    MIN(tp.start_time) AS premiere_participation,
    MAX(pl.end_time) AS derniere_action
FROM 
    players p
JOIN 
    players_in_parties pp ON p.id_player = pp.id_player
JOIN 
    players_play pl ON pp.id_players_in_parties = pl.id_players_in_parties
JOIN 
    turns tp ON pl.id_turn = tp.id_turn
GROUP BY 
    p.pseudo
ORDER BY 
    nombre_de_parties DESC, premiere_participation, derniere_action, nom_joueur;

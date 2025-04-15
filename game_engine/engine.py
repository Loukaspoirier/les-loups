from db import SessionLocal
from models import Player, PlayerInParty, Party, PlayerPlay
from sqlalchemy.exc import NoResultFound
from datetime import datetime

class GameEngineService:
    def __init__(self):
        self.db = SessionLocal()

    def register_player(self, pseudo, party_id):
        player = Player(pseudo=pseudo)
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)

        player_party = PlayerInParty(
            id_party=party_id,
            id_player=player.id_player,
            is_alive="true"
        )
        self.db.add(player_party)
        self.db.commit()
        self.db.refresh(player_party)

        return player.id_player

    def move_player(self, player_id, origin_col, origin_row, target_col, target_row):
        player_party = self.db.query(PlayerInParty).filter(PlayerInParty.id_player == player_id).first()
        if not player_party:
            raise Exception("Player not found in party.")

        # simuler un tour actif
        turn_id = 1

        play = PlayerPlay(
            id_players_in_parties=player_party.id_players_in_parties,
            id_turn=turn_id,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            action="MOVE",
            origin_position_col=origin_col,
            origin_position_row=origin_row,
            target_position_col=target_col,
            target_position_row=target_row
        )
        self.db.add(play)
        self.db.commit()
        return True

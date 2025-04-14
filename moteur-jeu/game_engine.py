# game_engine.py
from datetime import datetime
from db import SessionLocal
from models import *

class GameEngine:
    def __init__(self, id_party):
        self.id_party = id_party
        self.db = SessionLocal()
        self.turn = self.get_or_create_turn()
        self.obstacles = self.load_obstacles()

    def get_or_create_turn(self):
        last = self.db.query(Turn).filter_by(id_party=self.id_party).order_by(Turn.id_turn.desc()).first()
        if last and not last.end_time:
            return last
        new_turn = Turn(id_party=self.id_party, start_time=datetime.now())
        self.db.add(new_turn)
        self.db.commit()
        return new_turn

    def load_obstacles(self):
        obs = self.db.query(Obstacle).filter_by(id_party=self.id_party).all()
        return {(o.position_col, o.position_row) for o in obs}

    def get_player_position(self, pip_id):
        last_play = self.db.query(PlayerPlay).filter_by(id_players_in_parties=pip_id)\
            .order_by(PlayerPlay.id_turn.desc(), PlayerPlay.end_time.desc()).first()
        if last_play:
            return last_play.target_position_col, last_play.target_position_row
        return "0", "0"

    def compute_visible_cells(self, x, y):
        vision = ""
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                col, row = str(x + dx), str(y + dy)
                vision += "1" if (col, row) in self.obstacles else "0"
        return vision

    def process_input(self, json_data):
        try:
            move = json_data["move"]
            params = {k: v for p in move["parameters"] for k, v in p.items()}
            id_party = params["id_party"]
            id_player = params["id_player"]
            dx, dy = move["next_position"]["row"], move["next_position"]["col"]
            action = move["action"]

            pip = self.db.query(PlayerInParty).filter_by(id_party=id_party, id_player=id_player).first()
            if not pip:
                return {"status": "KO", "response": {"error": "Player not found"}}

            x0, y0 = self.get_player_position(pip.id_players_in_parties)
            x, y = int(x0) + dx, int(y0) + dy
            col, row = str(x), str(y)

            if (col, row) in self.obstacles:
                return {"status": "KO", "response": {"error": "Obstacle"}}

            now = datetime.now()
            play = PlayerPlay(
                id_players_in_parties=pip.id_players_in_parties,
                id_turn=self.turn.id_turn,
                start_time=now,
                end_time=now,
                action=action,
                origin_position_col=x0,
                origin_position_row=y0,
                target_position_col=col,
                target_position_row=row
            )
            self.db.add(play)
            self.db.commit()

            visible = self.compute_visible_cells(x, y)
            return {"status": "OK", "response": {"visible_cells": visible}}

        except Exception as e:
            self.db.rollback()
            return {"status": "KO", "response": {"error": str(e)}}

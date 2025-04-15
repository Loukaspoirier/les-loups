# models.py
from sqlalchemy import Column, Integer, Text, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db import Base

class Player(Base):
    __tablename__ = "players"
    id_player = Column(Integer, primary_key=True)
    pseudo = Column(Text)

class Party(Base):
    __tablename__ = "parties"
    id_party = Column(Integer, primary_key=True)
    title_party = Column(Text)

class Role(Base):
    __tablename__ = "roles"
    id_role = Column(Integer, primary_key=True)
    description_role = Column(Text)

class RoleQuota(Base):
    __tablename__ = "roles_quotas"
    id_party = Column(Integer, ForeignKey("parties.id_party"), primary_key=True)
    id_role = Column(Integer, ForeignKey("roles.id_role"), primary_key=True)
    min_quota = Column(Integer)
    max_quota = Column(Text)

class Obstacle(Base):
    __tablename__ = "obstacles"
    id_party = Column(Integer, ForeignKey("parties.id_party"), primary_key=True)
    id_obstacle = Column(Integer, primary_key=True)
    position_col = Column(Text)
    position_row = Column(Text)

class PlayerInParty(Base):
    __tablename__ = "players_in_parties"
    id_players_in_parties = Column(Integer, primary_key=True)
    id_party = Column(Integer, ForeignKey("parties.id_party"))
    id_player = Column(Integer, ForeignKey("players.id_player"))
    id_role = Column(Integer, ForeignKey("roles.id_role"))
    is_alive = Column(Text)

class Turn(Base):
    __tablename__ = "turns"
    id_turn = Column(Integer, primary_key=True)
    id_party = Column(Integer, ForeignKey("parties.id_party"))
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)

class PlayerPlay(Base):
    __tablename__ = "players_play"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_players_in_parties = Column(Integer, ForeignKey("players_in_parties.id_players_in_parties"))
    id_turn = Column(Integer, ForeignKey("turns.id_turn"))
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    action = Column(String(10))
    origin_position_col = Column(Text)
    origin_position_row = Column(Text)
    target_position_col = Column(Text)
    target_position_row = Column(Text)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "postgresql://user:password@localhost:5432/les-loups"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
SessionLocal = sessionmaker(bind=engine)

# Définition simplifiée pour "parties"
parties = Table(
    "parties", metadata,
    Column("id_party", Integer, primary_key=True),
    Column("title", String),
    Column("map_width", Integer),
    Column("map_height", Integer),
    Column("nb_players", Integer),
    Column("max_turns", Integer),
    Column("turn_duration_seconds", Integer),
    Column("nb_obstacles", Integer),
    Column("created_at", String),
)

app = FastAPI()

class PartyCreate(BaseModel):
    title: str
    map_width: int
    map_height: int
    nb_players: int
    max_turns: int
    turn_duration_seconds: int
    nb_obstacles: int

@app.post("/create-party")
def create_party(party: PartyCreate):
    db = SessionLocal()
    try:
        new_party = {
            "title": party.title,
            "map_width": party.map_width,
            "map_height": party.map_height,
            "nb_players": party.nb_players,
            "max_turns": party.max_turns,
            "turn_duration_seconds": party.turn_duration_seconds,
            "nb_obstacles": party.nb_obstacles,
            "created_at": datetime.datetime.now().isoformat()
        }
        insert_stmt = parties.insert().values(**new_party)
        result = db.execute(insert_stmt)
        db.commit()
        return {"status": "success", "id_party": result.inserted_primary_key[0]}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# flask_server.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/players')
def get_players():
    return jsonify([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])

if __name__ == '__main__':
    # Important : écouter sur 0.0.0.0 pour que ce soit accessible hors du conteneur
    app.run(host='0.0.0.0', port=5001)

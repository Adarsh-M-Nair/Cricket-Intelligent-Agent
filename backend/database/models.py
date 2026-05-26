from sqlalchemy import Column, Integer, String

from backend.database.db import Base


# ---------------------------------------------------
# Match Table
# ---------------------------------------------------

class Match(Base):

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)

    match_id = Column(String)

    date = Column(String)

    venue = Column(String)

    team1 = Column(String)

    team2 = Column(String)

    winner = Column(String)


# ---------------------------------------------------
# Delivery Table
# ---------------------------------------------------

class Delivery(Base):

    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)

    match_id = Column(String)

    innings = Column(Integer)

    over = Column(Integer)

    ball = Column(Integer)

    batter = Column(String)

    bowler = Column(String)

    runs = Column(Integer)
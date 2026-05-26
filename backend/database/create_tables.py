from db import engine, Base
from models import Match, Delivery

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
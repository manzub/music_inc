from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Jeddac401@localhost:5437/musicincapp"
SQLALCHEMY_TRACK_MODIFICATIONS = False

MANAGERS = [
  {"name": "Mom", "salary": 0, "effect": "Reduces artist signing cost"},
  {"name": "Ashley Stone", "salary": 5000, "effect": "Reduces artist signing cost"},
  {"name": "Marcus Lee", "salary": 3000, "effect": "Faster release schedule"},
  {"name": "Riley West", "salary": 1000, "effect": "Basic starter manager"},
]

LEVELS = [
  {"name": "Moms Garage", "price": 0, "artists": 1},
  {"name": "Small Office", "price": 50000, "artists": 2}
]

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def connect_db():
  return engine


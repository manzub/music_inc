import random
from sqlalchemy.orm import Session
from app.services.artist_service import generate_artists_random
from app.models.label import Label
from app.models.artist import Artist

def check_record_name(session: Session, name: str):
  check_label = session.query(Label).filter_by(name=name).first()
  if check_label is None:
    return name
  return False

def create_label_db(session: Session, name: str, userid: str):
  name = check_record_name(session, name)
  # random budget
  budget = random.choice([5000, 8000, 10000])
  label = Label(name=name, user=userid, budget=budget)
  session.add(label)
  session.commit()

  return label

def scout_artists(session: Session):
  artists = session.query(Artist).filter_by(label_id=None)
  if artists is not None:
    return artists
  generate_artists_random(5, session, scout_artists)
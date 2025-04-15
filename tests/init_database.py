import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import Label, Staff, Artist, Releases, ArtistDecisionHistory
from app.config.config import engine, Base, SessionLocal
from app.services.artist_service import save_decision, generate_artist_name, create_artist

session = SessionLocal()

def setup_staffs():
  # setup artists
  create_artist(session=session, name=generate_artist_name(), fee=1000)
  create_artist(session=session, name=generate_artist_name(), fee=3000)
  create_artist(session=session, name=generate_artist_name(), fee=4000)

# @pytest.fixture()
def init_db():
  print("🔄 Initializing database...")  # Debugging log
  try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
  except Exception as e:
    print(f"❌ Error creating tables: {e}")

if __name__ == '__main__':
  # init_db()
  setup_staffs()
  # artist = Artist(name=generate_artist_name(), popularity=3.6)
  # session.add(artist)
  # session.commit()
  # decision = artist.make_decision({1: 'no', 2: 'maybe', 3: 'yes'})
  # save_decision(session, artist, decision=decision)
  # print(f"{artist.name} to attend studio session: {decision}")
  # artist.train_model(session)
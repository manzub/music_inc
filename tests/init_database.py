from app.models.label import Label
from app.models.artist import Artist
from app.models.staff import Staff
from app.models.releases import Releases
from app.models.decision_history import ArtistDecisionHistory
from app.config.config import engine, Base, SessionLocal
from app.services.staff_service import add_staff
from app.services.artist_service import save_decision, generate_artist_name

session = SessionLocal()

def setup_staffs():
  add_staff(session=session, name="Mom", role="manager", salary=0)
  add_staff(session=session, name="Neighbourhood Admin", role="manager", salary=2000)
  add_staff(session=session, name="Chris", role="manager", salary=5000)

  # setup artists
  add_artist(session=session, name="Jenne", genre="rnb", popularity=3.5)
  add_artist(session=session, name="Mark", genre="hip-hop", popularity=5.5)
  add_artist(session=session, name="sade", genre="afrobeats", popularity=1.5)

def init_db():
  print("🔄 Initializing database...")  # Debugging log
  try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
  except Exception as e:
    print(f"❌ Error creating tables: {e}")

if __name__ == '__main__':
  # init_db()
  # setup_staffs()
  artist = Artist(name=generate_artist_name(), popularity=3.6)
  session.add(artist)
  session.commit()
  decision = artist.make_decision({1: 'no', 2: 'maybe', 3: 'yes'})
  save_decision(session, artist, decision=decision)
  print(f"{artist.name} to attend studio session: {decision}")
  artist.train_model(session)
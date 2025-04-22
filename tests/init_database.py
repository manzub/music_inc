import pymongo
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import Label, Staff, ArtistModel, Releases, ArtistDecisionHistory
from app.config.config import MONGODB_CONNECTION_STRING
from app.services.artist_service import save_decision, generate_artist_name, create_artist

def init_db():
  print("🔄 Initializing database...")  # Debugging log
  try:
    client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
    db = client["music_inc"]
    print("✅ Database tables created successfully!")
  except Exception as e:
    print(f"❌ Error creating tables: {e}")

if __name__ == '__main__':
  # init_db()
  # setup_staffs()
  db = pymongo.MongoClient(MONGODB_CONNECTION_STRING)["music_inc"]
  artists_collection = db["artists"]
  new_artist = ArtistModel(name=generate_artist_name(), popularity=3.6, fee=10000)
  artists_collection.insert_one(new_artist.to_dict())
  decision = new_artist.make_decision({1: 'no', 2: 'maybe', 3: 'yes'})
  save_decision(artists_collection, new_artist, decision=decision)
  # print(f"{artist.name} to attend studio session: {decision}")
  # artist.train_model(session)
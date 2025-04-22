import random
from pymongo.collection import Collection
from app.services.artist_service import generate_artists_random
from app.models.label import Label

def check_record_name(collection: Collection, name: str):
  check_label = collection.find_one({"name": name})
  if check_label is None:
    return name
  return False

def create_label_db(collection: Collection, name: str, userid: str):
  name = check_record_name(collection, name)
  # random budget
  budget = random.choice([5000, 8000, 10000])
  label = Label(name=name, user=userid, budget=budget)
  collection.insert_one(label.to_dict())

  return label

def scout_artists(collection: Collection):
  artists = collection.find({"label_id": None})
  if artists is not None:
    return artists
  generate_artists_random(collection=collection, count=5, callback=scout_artists)
import random
from datetime import datetime
from pymongo.collection import Collection
from app.models.artist import ArtistModel

def generate_artist_name():
  prefixes = ["Lil", "Big", "Young", "DJ", "MC", "King", "Queen", "Dr.", "Sir", "Prof."]
  adjectives = ["Savage", "Wicked", "Smooth", "Clever", "Loyal", "Reckless", "Silent", "Electric", "Famous"]
  nouns = ["Vibe", "Shadow", "Storm", "Fox", "Ace", "Legend", "Wave", "Knight", "Flame", "Beats", "Rhymes"]
  real_names = ["Jay", "Mike", "Chris", "Dani", "Nina", "Ty", "Jules", "Zane", "Luna", "Milo", "Sasha", "Kai"]

  style = random.randint(1,4)

  if style == 1:
    return f"{random.choice(prefixes)} {random.choice(nouns)}"
  elif style == 2:
    return f"{random.choice(adjectives)} {random.choice(nouns)}"
  elif style == 3:
    return f"{random.choice(real_names)} {random.choice(nouns)}"
  else:
    return f"{random.choice(prefixes)} {random.choice(real_names)}"

def generate_artists_random(collection: Collection, count: int, callback  = None):
  count = count if count else random.randint(1, 5)
  # generate random artists with different personalities
  for x in range(count):
    create_artist(collection=collection, name=generate_artist_name())
  if callback:
    callback(collection)

def create_artist(collection: Collection, name: str, fee: int = None):
  try:
    new_artist = ArtistModel(name, fee=fee if fee else random.randint(1000, 10000))
    collection.insert_one(new_artist.to_dict())
  except:
    print(f"Artist '{new_artist.name}' already exists. Skipping...")

def save_decision(collection: Collection, artist: ArtistModel, decision: int, event: str = "negotiation"):
  new_decision = {"event": event, "decision": decision, "timestamp": datetime.utcnow()}
  artist.decision_history.append(new_decision)
  update = {"$set": {"decision_history": artist.decision_history}}
  collection.update_one({"name": artist.name}, update)

def release_music(collection: Collection, artist: ArtistModel, release_type: str, featured: int, genre: str,):
  # releases - id, type[albuim,single], featured[artist,none], genre, sales
  # if release_type in ["album", "single"]:
  #   new_release = Releases(artist=artist.id, release_type=release_type, featured=featured, genre=genre)
  #   session.add(new_release)
  #   session.commit()
  pass
import random
from datetime import datetime
from rich.prompt import Prompt
from sqlalchemy.orm import Session
from app.models.artist import Artist
from app.models.releases import Releases
from app.models.decision_history import ArtistDecisionHistory

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

def generate_artists_random(session:Session, count: int, callback  = None):
  count = count if count else random.randint(1, 5)
  # generate random artists with different personalities
  for x in range(count):
    create_artist(session, generate_artist_name())
  if callback:
    callback(session)

def create_artist(session: Session, name: str, fee: int):
  new_artist = Artist(name, fee=fee)
  session.add(new_artist)
  session.commit()

def save_decision(session: Session, artist: Artist, decision: int):
  new_decision = ArtistDecisionHistory(artist_id=1, personality=artist.personality, decision=decision)
  session.add(new_decision)
  session.commit()

def release_music(session: Session, artist: Artist, release_type: str, featured: int, genre: str,):
  # releases - id, type[albuim,single], featured[artist,none], genre, sales
  if release_type in ["album", "single"]:
    new_release = Releases(artist=artist.id, release_type=release_type, featured=featured, genre=genre)
    session.add(new_release)
    session.commit()
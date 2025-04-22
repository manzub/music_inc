import random
import pandas as pd
from app.models.decision_history import ArtistDecisionHistory
from app.config.config import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship, Session
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# personalised artist that can make decisions and negotiations
# each artist has a personality that affects choice
# send choice options - 1 (good), 2 (neutral), 3 (bad/negative) based on personality traits artist will select random choice
class ArtistModel():
  def __init__(self, name: str, genre: str = None, popularity: float = None, personality: dict = None, fee: int = None, label_id = None):
    self.name = name
    self.genre = genre if genre else self.generate_genre()
    self.popularity = popularity if popularity else round(random.uniform(1.0, 3.0), 1)
    self.signed_date = datetime.utcnow()
    self.label_id = label_id
    self.personality = personality if personality else self.generate_personality()
    self.decision_history = []
    self.signing_fee = fee if fee else random.randint(1000, 10000)
    self.model = None

  def generate_genre(self):
    genres = ["hiphop", "randb", "country", "pop", "afrobeats", "jazz"]
    genre = random.choice(genres)
    return genre

  def generate_personality(self):
    traits = ["lazy", "disciplined", "arrogant", "humble", "impulsive"]
    return {trait: random.choice([True, False]) for trait in traits}

  def make_decision(self, choices):
    if self.model:
      features = [int(value) for value in self.personality.values()]
      decision_index = self.model.predict([features])[0]
      decision = list(choices.keys())[decision_index]
    else:
      decision = random.choice(list(choices.keys()))

    # save_decision
    return decision
  
  def train_model(self, session: Session):
    decisions = session.query(ArtistDecisionHistory).filter_by(artist_id=self.id).all()
    if len(decisions) < 5:  # Need at least 5 data points to train
      return
    
    # prepare dataframe
    df = pd.DataFrame([(d.personality, d.decision) for d in decisions], columns=["personality", "decision"])
    df["personality"] = df["personality"].apply(eval)  # Convert string to dict
    df = df.join(pd.json_normalize(df["personality"])).drop(columns=["personality"])

    # Encode decision labels
    label_encoder = LabelEncoder()
    df["decision"] = label_encoder.fit_transform(df["decision"])

    # Train Decision Tree model
    X = df.drop(columns=["decision"])
    y = df["decision"]
    model = DecisionTreeClassifier()
    model.fit(X, y)

    self.model = model  # Save trained model

  def to_dict(self):
    return {
      "name": self.name,
      "genre": self.genre,
      "popularity": self.popularity,
      "signed_date": self.signed_date,
      "label_id": self.label_id,
      "personality": self.personality,
      "decision_history": self.decision_history,
      "signing_fee": self.signing_fee
    }
  
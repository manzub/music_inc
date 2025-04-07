from config.config import Base
from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey, String
from datetime import datetime


class ArtistDecisionHistory(Base):
  __tablename__ = "decision_history"

  id = Column(Integer, primary_key=True, index=True)
  artist_id = Column(Integer, ForeignKey("artists.id"))
  personality = Column(JSON, default={})
  decision = Column(String, nullable=False)
  timestamp = Column(DateTime, default=datetime.now)

  def __init__(self, artist_id, personality, decision):
    self.artist_id = artist_id
    self.personality = personality
    self.decision = decision
    self.timestamp = datetime.now()
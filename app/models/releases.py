from config.config import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime

class Releases(Base):
  __tablename__ = "releases"

  id = Column(Integer, primary_key=True, index=True)
  artist_id = Column(Integer, ForeignKey("artists.id"))
  release_type = Column(String(7), nullable=False, default="single")
  featured_id = Column(Integer, nullable=True)
  genre = Column(String, nullable=False)
  sales = Column(Float, default=0.0)

  def __init__(self, artist, release_type, featured, genre):
    self.release_type = release_type
    self.artist_id = artist
    self.featured_id = featured
    self.genre = genre
    self.sales = 0.0
from app.config.config import Base
from sqlalchemy import Column, String, Integer, DateTime, func

def fetch_label(owner):
  return Label.query.get(owner)

class Label(Base):
  __tablename__ = "record_labels"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, nullable=False)
  user = Column(String, unique=True, nullable=False)
  budget = Column(Integer, default=0)
  level = Column(Integer, default=1)
  # status conditions 0 = bankrupt, 1 = active,
  status = Column(Integer, default=1)

  # Automatically set timestamps
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  def __init__(self, name: str, user: str, budget: int):
    self.name = name
    self.user = user
    self.budget = budget

  def check_userid(self, userid):
    return userid == self.user
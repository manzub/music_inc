import random
import string
from app.config.config import Base
from sqlalchemy import Column, String, Integer, DateTime, func

def fetch_label(owner):
  return Label.query.get(owner)

class Label(Base):
  __tablename__ = "record_labels"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, nullable=False)
  user = Column(String, unique=True, nullable=False)
  manager = Column(String, default=None)
  budget = Column(Integer, default=0)
  level = Column(Integer, default=1)
  # status conditions 0 = bankrupt, 1 = active,
  status = Column(Integer, default=1)

  # Automatically set timestamps
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  def __init__(self, name: str, user: str, budget: int, manager:str = None, level = None, status = None):
    self.name = name
    self.user = self.create_userid()
    self.budget = budget
    self.manager = manager
    self.level = level
    self.status = status
  
  def create_userid(self):
    characters = string.ascii_letters + string.digits
    userid = ''.join(random.choice(characters) for _ in range(random.randint(6, 9)))
    return userid
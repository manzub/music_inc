import random

from app.config.config import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Staff(Base):
  __tablename__ = "staffs"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, nullable=False)
  role = Column(String, nullable=False)
  salary = Column(Integer, nullable=False)
  effect = Column(String, nullable=False)
  label_id = Column(Integer, ForeignKey("record_labels.id"))

  label = relationship("Label", backref="staffs")

  def __init__(self, name: str, role: str, salary: int, effect: str = None):
    self.name = name
    self.role = role
    self.salary = salary
    self.effect = effect if effect else self.random_effect()

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "role": self.role,
      "salary": self.salary,
      "effect": self.effect
    }
  
  def random_effect(self):
    effects = ["Reduces artist signing cost", "Faster release schedule", "Reduces signing cost"]
    return random.choice(effects)
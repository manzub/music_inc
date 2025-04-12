from app.config.config import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Staff(Base):
  __tablename__ = "staffs"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, nullable=False)
  role = Column(String, nullable=False)
  salary = Column(Integer, nullable=False)
  label_id = Column(Integer, ForeignKey("record_labels.id"))

  label = relationship("Label", backref="staffs")

  def __init__(self, name: str, role: str, salary: int):
    self.name = name
    self.role = role
    self.salary = salary
import random
from bson.objectid import ObjectId
import string

class Label():
  def __init__(self, name: str, user: str, budget: int, manager: str = None, level: int = 0, status: int = 1):
    self.name = name
    self.user = user if user else self.create_userid()
    self.budget = budget
    self.manager = manager
    self.staff: list[ObjectId] = []
    self.signed_artists = []
    self.level = level
    self.status = status
  
  def create_userid(self):
    characters = string.ascii_letters + string.digits
    userid = ''.join(random.choice(characters) for _ in range(random.randint(4, 6)))
    return userid
  
  def to_dict(self):
    return {
      "name": self.name,
      "user": self.user,
      "budget": self.budget,
      "manager": self.manager,
      "staff": self.staff,
      "signed_artists": self.signed_artists,
      "level": self.level,
      "status": self.status
    }
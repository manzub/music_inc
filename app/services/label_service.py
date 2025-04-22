import random
from app.models import labels_collection, Label

def check_record_name(name: str):
  check_label = labels_collection.find_one({"name": name})
  if check_label is None:
    return name
  return False

def create_label_db(name: str, userid: str):
  name = check_record_name(name)
  # random budget
  budget = random.choice([5000, 8000, 10000])
  label = Label(name=name, user=userid, budget=budget)
  labels_collection.insert_one(label.to_dict())

  return label
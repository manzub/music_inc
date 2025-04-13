from rich.console import Console
from rich.prompt import Prompt
from sqlalchemy.orm import Session
from app.models.staff import Staff
from app.models.label import Label

def scout_staffs(session: Session, role: str):
  # search staffs in database
  found_staffs = session.query(Staff).filter_by(role=role)
  return found_staffs

def choice_staff(staffs: Staff):
  print("Available staffs...")
  for i, item in enumerate(staffs):
    print(f"{i}. {item.name} - ${item.salary}")
  choice = Prompt.ask('Enter your choice... ')
  return choice

def add_staff(session: Session, name: str, role: str, salary: int):
  staff = Staff(name=name, role=role, salary=salary)
  session.add(staff)
  session.commit()
  return staff

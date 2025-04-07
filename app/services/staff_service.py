from rich.console import Console
from rich.prompt import Prompt
from sqlalchemy.orm import Session
from models.staff import Staff
from models.label import Label

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


def sign_manager(session: Session, label: Label):
  managers = session.query(Staff).filter_by(role="manager")
  if managers is not None:
    choice = choice_staff(staffs=managers)
    if choice is not None and choice.isnumeric():
      selected = None
      for i,x in enumerate(managers):
        if int(choice) is i:
          selected = x
          break

      manager = session.get(Staff, selected.id)
      label = session.get(Label, label.id)

      prompt = Prompt.ask(f"Are you sure you want to sign {selected.name}", choices=["yes","no"], default="yes")
      if prompt.lower() in ["yes", "y"]:
        manager.label_id = label.id
        label.budget = label.budget - manager.salary
        session.commit()

def add_staff(session: Session, name: str, role: str, salary: int):
  staff = Staff(name=name, role=role, salary=salary)
  session.add(staff)
  session.commit()
  return staff

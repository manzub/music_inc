from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt
from app.models import Label, Staff
from app.config.config import MANAGERS
from app.services.label_service import check_record_name, create_label_db

console = Console()

def create_label_func(session: Session):
  name = Prompt.ask("[cyan]Enter your label name to begin... [cyan]")

  if check_record_name(session, name):
    label = create_label_db(session, name=name, userid=None)
    console.print(f"\n💰 Your starting budget is: [bold cyan]${label.budget}[/bold cyan]")

    # select managers
    console.print("\n🧑‍💼 [bold]Choose a Manager:[/bold]")
    for idx, manager in enumerate(MANAGERS, start=1):
      console.print(f"{idx}. {manager['name']} ({manager['salary']}) - {manager['effect']}")
    
    choice = Prompt.ask("Pick your manager", choices=[str(i) for i in range(1, len(MANAGERS)+1)])
    selected_manager = MANAGERS[int(choice) - 1]
    console.print(f"Signed Manager: {selected_manager['name']}")

    remaining_budget = label.budget - selected_manager["salary"]
    label.budget = remaining_budget
    label.manager = selected_manager["name"]
    session.commit()

    console.print(f"\n🏷️ Created Record Label: [bold magenta]{label.name}[/bold magenta] with ${remaining_budget} and manager [bold]{selected_manager['name']}[/bold]")

    return label
  else:
    console.print("[red]That Record Name already exists.. try again[red]")
    create_label_func(session=session)

def create_label(session: Session):
  console.print("\n\nI see you want to start a record label, do you have what it takes?")
  console.print("Manage Artsits, Paparazzo, Scandals and all the drama involved!")
  console.print("See you at the top!...\n\n")
  create_label_func(session=session)
  

def load_label(session: Session):
  userid = Prompt.ask("[cyan]Enter your userid... [cyan]")
  
  if userid is not None:
    found = session.query(Label).filter_by(user=userid).first()
    if not found:
      console.print(f"[red]User ID - {userid} not found!... try again[red]")
      load_label(session)
    
    console.print(f"Found ${found.name} ⭐️✨")
    label = Label(found.name, userid, found.budget, found.level, found.status)
    return label
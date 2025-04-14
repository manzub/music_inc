from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt, Confirm
from app.models import Label, Staff
from app.config.config import MANAGERS, LEVELS
from app.services.label_service import check_record_name, create_label_db

console = Console()

def select_manager(label: Label):
  console.print("\n🧑‍💼 [bold]Choose a Manager:[/bold]")
  for idx, manager in enumerate(MANAGERS, start=1):
    if label.manager is not manager["name"]:
      console.print(f"{idx}. {manager['name']} ({manager['salary']}) - {manager['effect']}")
  console.print("Q. Exit")

  choice = Prompt.ask("Pick your manager", choices=[str(i) for i in range(1, len(MANAGERS)+1)]+["q"])
  selected_manager = MANAGERS[int(choice) - 1] if choice.isnumeric() else None
  return selected_manager

def create_label_func(session: Session):
  name = Prompt.ask("[cyan]Enter your label name to begin... [cyan]")

  if check_record_name(session, name):
    label = create_label_db(session, name=name, userid=None)
    console.print(f"\n💰 Your starting budget is: [bold cyan]${label.budget}[/bold cyan]")

    # select managers
    selected_manager =  select_manager(label=label)
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
    label = Label(name=found.name, user=userid, budget=found.budget, manager=found.manager, level=found.level, status=found.status)
    return label
  
def manage_label(session: Session, label: Label):
  console.print("\n[bold blue]🏠 Manage Label/Staffs[/bold blue]")
  console.print(f"[magenta]{label.name} - 💰 ${label.budget} (Manager: {label.manager}) Level: {label.level}/5[magenta]")
  console.print("======================================")
  # print progress bar
  percent = int((label.level / 5) * 100)
  filled_length = int(30 * label.level // 5)
  bar = "█" * filled_length + '-' * (30 - filled_length)
  console.print(f"Level {label.level}/{5} |{bar}| {percent}%")
  console.print("======================================")
  # progress bar end

  console.print("1. Manager")
  console.print("2. Lawyer")
  console.print("3. Office")
  console.print("4. Return to Main Menu")

  choice = Prompt.ask("\nChoose an action", choices=["1", "2", "3", "4"])

  if choice == "1":
    console.print("\n[bold green]📋 Current Manager:[/bold green]")
    if label.manager:
      console.print(f"🧑‍💼 {label.manager}")
    else:
      console.print("No manager assigned.")
    if Confirm.ask("Would you like to hire a manager?"):
      selected_manager = select_manager(label)
      if selected_manager is None:
        return
      if label.budget > selected_manager["salary"]:
        label.manager = selected_manager["name"]
        label.budget = label.budget - selected_manager["salary"]
      session.commit()
      console.print(f"[green]✅ Hired {selected_manager['name']} as your manager![/green]")
  elif choice == "2":
    console.print("\n[bold green]⚖️ Lawyer Management[/bold green]")
    console.print("This feature is under development.")
    # TODO: handle contract disputes or negotiations
  elif choice == "3":
    console.print("\n[bold green]🏢 Office[/bold green]")
    console.print(f"Current office is: {LEVELS[label.level]['name']}.")
    next_level = LEVELS[label.level + 1]
    if Confirm.ask(f"Would you like to upgrade for ${next_level['price']}?"):
      if label.budget >= next_level['price']:
        label.budget -= next_level['price']
        label.level += 1
        session.commit()
        console.print("[green]🏢 Office upgraded! You now have a better working environment.[/green]")
        console.print(f"[green]You can now sign {next_level['artists']} artists.")
      else:
        console.print("[red]❌ Not enough budget to upgrade the office.[/red]")
  elif choice == "4":
    console.print("[yellow]Returning to main menu...[/yellow]")
    return
  
  # Loop again after action
  if Confirm.ask("\nDo you want to continue managing the label?"):
      manage_label(session, label)
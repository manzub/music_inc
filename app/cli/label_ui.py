from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt, Confirm
from app.models import Label, Artist
from app.config.config import MANAGERS, LEVELS
from app.services.label_service import check_record_name, create_label_db

console = Console()

# misc re-usable function to select manager loop
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
    console.print(f"Your User ID is {label.user} You will need this to login")

    return label
  else:
    console.print("[red]That Record Name already exists.. try again[red]")
    create_label_func(session=session)

# create label ui function
def create_label(session: Session):
  console.print("\n\nI see you want to start a record label, do you have what it takes?")
  console.print("Manage Artsits, Paparazzo, Scandals and all the drama involved!")
  console.print("See you at the top!...\n\n")
  return create_label_func(session=session) # create label game logic
  

# load label from DB and initialise saved modules
def load_label(session: Session):
  userid = Prompt.ask("[cyan]Enter your userid... [cyan]")
  
  if userid is not None:
    found = session.query(Label).filter_by(user=userid).first()
    if not found:
      console.print(f"[red]User ID - {userid} not found!... try again[red]")
      return None
    
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
    # TODO: sign a lawyer **NEEDED** to negotiate with artists
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

def scout_sign_artist(session: Session, label: Label):
  # scout artist
  signed_count = len(label.signed_artists) if label.signed_artists else 0
  can_sign_artist = LEVELS[label.level]["artists"] > signed_count
  if can_sign_artist: # can sign new artist
    artists = session.query(Artist).all()
    console.print("\n🧑‍💼 [bold]Choose an Artist:[/bold]")

    signed_artists = label.signed_artists or []
    available_artists = [a for a in artists if a.id not in signed_artists]
    if not available_artists:
      console.print("[red]No unsigned artists available.[/red]")
      return None

    for idx, artist in enumerate(available_artists, start=1):
      traits = artist.personality.keys()
      traits_str = ", ".join(traits).replace("_", " ").title()
      console.print(f"{idx}. {artist.name}[Fee: {artist.signing_fee}] - Genre: ({artist.genre}/{artist.popularity}) - Personality: {traits_str}")
    console.print("Q. Exit")

    valid_choices = [str(i) for i in range(1, len(available_artists)+1)] + ["q"]
    choice = Prompt.ask("Pick an artist", choices=valid_choices)

    if choice.lower() == "q":
      return None
    
    selected_artist = available_artists[int(choice) - 1]

    # sign artist
    if label.budget > selected_artist.signing_fee:
      label.budget -= selected_artist.signing_fee
      if not label.signed_artists:
        label.signed_artists = []
      label.signed_artists.append(selected_artist.id)
      session.commit()

      console.print(f"\n\n[green]✅ Signed Artist: {selected_artist.name}!🎉🎉🎉[green]")
    else:
      console.print(f"[red]❌ Insufficient funds to sign this artist. Balance is: {label.budget}[red]")
      return None
  else:
    console.print("[yellow]Already signed MAX allowed artists. looks like we need a bigger office!😮[yellow]")
from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt
from app.models.label import Label
from app.cli.label_ui import manage_label, scout_sign_artist
from app.cli.artist_ui import select_artist_menu, manage_artist

console = Console()

def main_menu(session: Session, label: Label,  existing = False):
  console.print("\n🎵 [bold magenta]Welcome to Music Inc: CLI Edition[/bold magenta] 🎵")
  if existing:
    console.print(f"Welcome back {label.name} 🤩")
  
  while True:
    console.print("\n[bold blue]🏠 Main Menu[/bold blue]")
    console.print(f"[magenta]{label.name} - 💰 ${label.budget} (Manager: {label.manager}) Level: {label.level}/5[magenta]")
    console.print("======================================")
    console.print("1. Scout & Sign New Artist")
    console.print("2. Manage Signed Artists")
    console.print("3. Check News & Social Feed")
    console.print("4. Manage Label & Staff")
    console.print("5. Exit Game")

    choice = Prompt.ask("\nChoose an action", choices=["1", "2", "3", "4", "5"])

    if choice == "1":
      scout_sign_artist(session=session, label=label)
    elif choice == "2":
      # TODO: manage signed artists
      # release music, manage contracts, manage fans, tour
      artist = select_artist_menu(session=session, label=label)
      manage_artist(artist=artist, session=session)
    elif choice == "3":
      # TODO: check news & social feed
      # manage paparazo, gossip about signed artists, rivals
      pass
    elif choice == "4":
      manage_label(session, label)
    elif choice == "5":
      # TODO: save progress
      console.print("[red]Saving progress and exiting... See you at the top![/red]")
      break

    session.close()
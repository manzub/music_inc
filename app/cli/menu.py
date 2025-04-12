from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt
from app.models.label import Label

console = Console()

def main_menu(session: Session, label: Label,  existing = False):
  console.print("\n🎵 [bold magenta]Welcome to Music Inc: CLI Edition[/bold magenta] 🎵")
  if existing:
    console.print(f"Welcome back {label.name} 🤩")
  
  while True:
    console.print("\n[bold blue]🏠 Main Menu[/bold blue]")
    console.print("1. Scout & Sign New Artist")
    console.print("2. Manage Signed Artists")
    console.print("3. Check News & Social Feed")
    console.print("4. Manage Label & Staff")
    console.print("5. Exit Game")

    choice = Prompt.ask("\nChoose an action", choices=["1", "2", "3", "4", "5"])

    if choice == "5":
      console.print("[red]Saving progress and exiting... See you at the top![/red]")
      break

    session.close()
import random
import string
from app.config.config import SessionLocal
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from app.models.label import Label
from app.models.staff import Staff
from app.services.label_service import create_label
from app.services.staff_service import sign_manager

# start console
# create a new session
session = SessionLocal()
console = Console()

# start game
def game():
  console.print("\n[bold cyan]🎶 Welcome to Music Inc! 🎶[/bold cyan]")
  console.print("1. Start a new game")
  console.print("2. Load game")
  console.print("3. Exit")

  choice = Prompt.ask("\nChoose an option", choices=["1", "2", "3"])

  if choice == "1":
    from app.cli.label_ui import create_label
    create_label()
  elif choice == "2":
    console.print("[yellow]🔄 Loading game...[/yellow]")
    # fetch user id and load game
  else:
    console.print("[red]👋 Exiting... Goodbye![/red]")
    exit()

if __name__ == '__main__':
  game()

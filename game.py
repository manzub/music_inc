from app.config.config import SessionLocal
from rich.console import Console
from rich.prompt import Prompt
from app.models import Label, Staff
from app.cli.label_ui import create_label, load_label
from app.cli.menu import main_menu

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
    label = create_label(session=session)
    main_menu(label, False)
  elif choice == "2":
    console.print("[yellow]🔄 Loading game...[/yellow]")
    label = load_label(session)
    main_menu(label, True)
  else:
    console.print("[red]👋 Exiting... Goodbye![/red]")
    exit()

if __name__ == '__main__':
  game()

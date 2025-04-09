import random
import string
from config.config import SessionLocal
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from models.label import Label
from models.staff import Staff
from services.label_service import create_label
from services.staff_service import sign_manager

# start console
# create a new session
session = SessionLocal()
console = Console()

# start game
def game():
  pass

if __name__ == '__main__':
  game()

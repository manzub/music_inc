from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt
from app.models.label import Label

console = Console()

def create_label():
  pass

def load_label(session: Session):
  userid = Prompt.ask("[cyan]Enter your userid... [cyan]")
  
  if userid is not None:
    found = session.query(Label).filter_by(user=userid).first()
    if not found:
      console.print(f"[red]User ID - ${userid} not found!... try again[red]")
      load_label(session)
    
    console.print(f"Found ${found.name} ⭐️✨")
    label = Label(found.name, userid, found.budget, found.level, found.status)
    return label
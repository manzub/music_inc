from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt, Confirm
from app.models import Label, Artist, Staff

console = Console()

def select_artist_menu(session: Session, label: Label):
  console.print("\n[bold blue]🏠 Manage Signed Artists[/bold blue]")
  console.print("======================================")
  # print signed artists
  console.print("[yellow]Signed Artists: [yellow]")
  signed_artists = label.signed_artists if label.signed_artists else []
  available_artists: list[Artist] = []
  if len(signed_artists) > 0:
    for idx, item in enumerate(signed_artists, start=1):
      artist = session.query(Artist).filter_by(id=item).first()
      new_artist = Artist(artist.name, genre=artist.genre, popularity=artist.popularity, personality=artist.personality, fee=artist.signing_fee)
      available_artists.append(new_artist)
      console.print(f"{idx}. {artist.name} ({artist.genre})")
  else:
    console.print("No available artists at this moment.")
  console.print("Q. Exit")

  choice = Prompt.ask("Chose an artist:", choices=[str(i) for i in range(1, len(available_artists)+1)]+["q"]).lower()
  if not choice.isnumeric(): return None
  selected_artist = available_artists[int(choice) - 1]
  return selected_artist

def manage_artist(session: Session, artist: Artist):
  console.print(f"\n[bold green]🎤 Managing Artist: {artist.name}[/bold green]")
  console.print("1. Release Music")
  console.print("2. Manage Contracts")
  console.print("3. Fans & Tour")
  console.print("Q. Go Back")

  choice = Prompt.ask("\nChoose an action", choices=["1", "2", "3", "q"], default="q").lower()
  if choice == "1":
    release_music(session, artist)
  elif choice == "2":
    # manage_contracts(session, artist)
    pass
  elif choice == "3":
    # manage_fans(session, artist)
    pass
  elif choice == "q":
    return None
  

def release_music(session: Session, artist: Artist):
  pass

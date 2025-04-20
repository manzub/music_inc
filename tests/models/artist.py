import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.models import Artist
from app.services import artist_service



if __name__ == "__main__":
  artist = Artist(artist_service.generate_artist_name())
  print(dict(artist))
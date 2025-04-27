import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.models import artists_collection
from app.services.artist_service import generate_artists_random

    

if __name__ == "__main__":
  generate_artists_random(artists_collection, 2)
from pymongo import MongoClient
from app.config.config import MONGODB_CONNECTION_STRING

from .label import Label
from .artist import ArtistModel
from .releases import Releases

client = MongoClient(MONGODB_CONNECTION_STRING)
db = client["music_inc"]
# collections
labels_collection = db["labels"]
artists_collection = db["artists"]
releases_collection = db["releases"]
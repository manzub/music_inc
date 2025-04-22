class Releases():
  def __init__(self, artist, release_type, featured, genre):
    self.release_type = release_type
    self.artist_id = artist
    self.featured_id = featured
    self.genre = genre
    self.sales = 0.0
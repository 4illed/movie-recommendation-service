class Movie:
    def __init__(self, title, genre, popularity):
        self.title = title
        self.genre = genre
        self.popularity = popularity

    def __str__(self):
        return f"Title: {self.title}, Genre: {self.genre}"

    def to_dict(self):
        return {"title": self.title, "genre": self.genre, "popularity": self.popularity}

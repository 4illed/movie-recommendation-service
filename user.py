class User:
    def __init__(self, id, favorite_genre):
        self.id = id
        self.favorite_genre = favorite_genre

    def to_dict(self):
        return {"id": self.id, "favorite_genre": self.favorite_genre}

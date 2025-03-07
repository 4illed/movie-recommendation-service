import unittest
from main import app, movies, Movie


class TestRecommendations(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        movies.clear()
        movies.append(Movie(title="Inception", genre="Sci-Fi", popularity=95))
        movies.append(Movie(title="The Dark Knight", genre="Action", popularity=98))
        movies.append(Movie(title="Interstellar", genre="Sci-Fi", popularity=97))
        movies.append(Movie(title="The Matrix", genre="Sci-Fi", popularity=96))
        movies.append(Movie(title="Titanic", genre="Drama", popularity=94))
        movies.append(Movie(title="Venom", genre="Action", popularity=93))

    def test_get_recommendations(self):
        response = self.app.get("/recommendations")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]["title"], "The Dark Knight")
        self.assertEqual(data[1]["title"], "Interstellar")
        self.assertEqual(data[2]["title"], "The Matrix")
        self.assertEqual(data[3]["title"], "Inception")
        self.assertEqual(data[4]["title"], "Titanic")


if __name__ == "__main__":
    unittest.main()

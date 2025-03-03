import unittest
from main import app, movies


class MoviesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        movies.clear()

    def test_get_movies_empty(self):
        response = self.app.get("/movies")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def test_add_movie(self):
        movie_data = {"title": "Inception", "genre": "Sci-Fi", "popularity": 90}
        response = self.app.post("/movies", json=movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("title"), "Inception")
        self.assertEqual(data.get("genre"), "Sci-Fi")
        self.assertEqual(data.get("popularity"), 90)

        response = self.app.get("/movies")
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get("title"), "Inception")


if __name__ == "__main__":
    unittest.main()

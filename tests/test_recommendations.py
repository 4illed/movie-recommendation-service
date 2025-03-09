import unittest
from main import app, movies, users, Movie
from user import User


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


class TestRecommendationsGenre(unittest.TestCase):
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

    def test_get_recommendations_genre(self):
        response = self.app.post("/recommendations/genre", json={"genre": "Sci-Fi"})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["title"], "Inception")
        self.assertEqual(data[1]["title"], "Interstellar")
        self.assertEqual(data[2]["title"], "The Matrix")

    def test_get_recommendations_genre_not_found(self):
        response = self.app.post("/recommendations/genre", json={"genre": "Fantasy"})
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["error"], "No movies found in this genre")


class FavoriteMovieRecommendationTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

        users.clear()
        movies.clear()

        users.append(User(id=1, favorite_genre="Action"))
        users.append(User(id=2, favorite_genre="Sci-Fi"))

        movies.append(Movie(title="Spider-Man", genre="Action", popularity=9))
        movies.append(Movie(title="Venom", genre="Action", popularity=8))
        movies.append(Movie(title="Iron Man", genre="Sci-Fi", popularity=10))
        movies.append(
            Movie(title="Guardians of the Galaxy", genre="Sci-Fi", popularity=7)
        )

    def test_recommendations_by_favorite_success(self):
        response = self.client.post("/recommendations/favorite", json={"user_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {"title": "Spider-Man", "genre": "Action", "popularity": 9},
                {"title": "Venom", "genre": "Action", "popularity": 8},
            ],
        )

    def test_recommendations_by_favorite_user_not_found(self):
        response = self.client.post("/recommendations/favorite", json={"user_id": 999})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "User not found"})

    def test_recommendations_by_favorite_no_movies(self):
        users.append(User(id=3, favorite_genre="Horror"))
        response = self.client.post("/recommendations/favorite", json={"user_id": 3})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json, {"error": "No movies found for your favorite genre"}
        )

    def test_recommendations_by_favorite_missing_user_id(self):
        response = self.client.post("/recommendations/favorite", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "User ID not provided"})


class MovieSearchTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

        movies.clear()

        movies.append(Movie(title="Spider-Man", genre="Action", popularity=9))
        movies.append(Movie(title="Venom", genre="Action", popularity=8))
        movies.append(Movie(title="Iron Man", genre="Sci-Fi", popularity=10))
        movies.append(
            Movie(title="Guardians of the Galaxy", genre="Sci-Fi", popularity=7)
        )

    def test_get_movie_by_title_success(self):
        response = self.client.get("/movies/Spider-Man")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"title": "Spider-Man", "genre": "Action", "popularity": 9}
        )

    def test_get_movie_by_title_not_found(self):
        response = self.client.get("/movies/Avengers")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Movie not found"})


if __name__ == "__main__":
    unittest.main()

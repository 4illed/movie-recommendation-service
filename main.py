from flask import Flask, request, jsonify
from movie import Movie

app = Flask(__name__)

# Хранилище данных
movies = []
users = []


# GET /movies — возвращает список всех фильмов
@app.route("/movies", methods=["GET"])
def get_movies():
    return jsonify([movie.to_dict() for movie in movies])


# POST /movies — добавляет новый фильм
@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json()
    # Предполагается, что data содержит title, genre и popularity
    movie = Movie(
        title=data.get("title"),
        genre=data.get("genre"),
        popularity=data.get("popularity", 0),
    )
    movies.append(movie)
    return jsonify(movie.to_dict()), 201


# GET /recommendations — возвращает список популярных фильмов
@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    # Например, сортировка по убыванию популярности, берем топ 5
    sorted_movies = sorted(movies, key=lambda movie: movie.popularity, reverse=True)
    top_movies = sorted_movies[:5]
    return jsonify([movie.to_dict() for movie in top_movies])


# POST /recommendations/genre — составляет список фильмов указанного жанра
@app.route("/recommendations/genre", methods=["POST"])
def recommendations_by_genre():
    data = request.get_json()
    genre = data.get("genre")
    if genre is None:
        return jsonify({"error": "Genre not provided"}), 400

    filtered_movies = [movie for movie in movies if movie.genre == genre]
    if not filtered_movies:
        return jsonify({"error": "No movies found in this genre"}), 404
    return jsonify([movie.to_dict() for movie in filtered_movies])


# POST /recommendations/favorite — подбирает фильмы на основе предпочтений пользователя
@app.route("/recommendations/favorite", methods=["POST"])
def recommendations_by_favorite():
    data = request.get_json()
    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "User ID not provided"}), 400

    # Поиск пользователя по user_id

    # Подбор фильмов по предпочтительному жанру пользователя

    ...


# GET /movies/<title> — ищет информацию о фильме по названию
@app.route("/movies/<string:title>", methods=["GET"])
def get_movie_by_title(title): ...


if __name__ == "__main__":
    app.run(debug=True)

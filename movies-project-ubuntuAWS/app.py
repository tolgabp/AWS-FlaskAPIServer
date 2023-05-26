from flask import Flask, jsonify, request, render_template, redirect

app = Flask(__name__)

movies = [
    {
        "id": 1,
        "title": "Matrix",
        "director": "Lana Wachowski",
        "genre": "sci-fi",
        "date": 1999,
        "rating": 8.7,
    },
    {
        "id": 2,
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "genre": "sci-fi",
        "date": 2010,
        "rating": 8.6,
    },
]


# curl http://localhost:5000
@app.get("/")
def index():
    return render_template("index.html", user="Neo", movies=movies)


# curl http://localhost:5000/movies
@app.get("/movies")
def hello():
    return jsonify(movies)


# curl http://localhost:5000/movie/1
@app.get("/movie/<int:id>")
def get_movie(id):
    for movie in movies:
        if movie["id"] == id:
            return jsonify(movie)
    return f"Movie with id {id} not found", 404


# curl http://localhost:5000/add_movie --request POST --data '{"id":3,"director":"aaa","title":"bbb","rating":99.99}' --header "Content-Type: application/json"
@app.post("/add_movie")
def add_movie():
    new_id = int(request.form["id"])
    new_title = request.form["title"]
    new_director = request.form["director"]
    new_genre = request.form["genre"]
    new_date = int(request.form["date"]) ,
    new_rating = float(request.form["rating"])
    new_movie = {
        "id": new_id,
        "title": new_title,
        "director": new_director,
        "genre": new_genre,
        "date": new_date,
        "rating": new_rating,
    }
    movies.append(new_movie)
    return redirect("/")


# curl http://localhost:5000/update_movie/2 --request POST --data '{"director":"ccc","title":"ddd","rating":999.99}' --header "Content-Type: application/json"
@app.route("/update_movie/<int:id>", methods=["GET", "POST"])
def update_movie(id):
    for movie in movies:
        if movie["id"] == id:
            if request.method == "POST":
                movie["id"] = int(request.form["id"])
                movie["title"] = request.form["title"]
                movie["director"] = request.form["director"]
                movie["genre"] = request.form["genre"]
                movie["date"] = int(request.form["date"])
                movie["rating"] = float(request.form["rating"])
                return redirect("/")
            else:
                return render_template("update.html", movie=movie)
    return f"Movie with id {id} not found", 404


# curl http://localhost:5000/delete_movie/1 --request DELETE
@app.route("/delete_movie/<int:id>", methods=["GET", "POST"])
def delete_movie(id):
    for movie in movies:
        if movie["id"] == id:
            if request.method == "POST":
                movies.remove(movie)
                return redirect("/")
            else:
                return render_template("delete.html", movie=movie)
    return f"Movie with id {id} not found", 404
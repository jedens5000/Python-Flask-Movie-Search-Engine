from flask import Flask, redirect, render_template, url_for, request, session, redirect, flash
import requests
import os


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
apiKey = os.getenv("API_KEY")

@app.route("/")
def main():
    rawData = requests.get(
        "http://www.omdbapi.com/?apikey=" + apiKey + "&s=punk")
    movies = rawData.json()
    return render_template("home.html", movies=movies)


@app.route("/<title>")
def movies_by_title(title):
    rawData = requests.get("http://www.omdbapi.com/?apikey=" + apiKey + "&s="+title)
    movies = rawData.json()
    return render_template("home.html", movies=movies)


@app.route("/single_movie/<title>")
def single_movie(title):
    rawData = requests.get("http://www.omdbapi.com/?apikey=" + apiKey + "&t="+title)
    movie = rawData.json()
    return render_template("single_movie.html", movie=movie)


@app.route("/search")
def search_form():
    return render_template("search.html")


@app.route("/search_by_title", methods=["POST"])
def search_by_title():
    title = request.form["title"]
    year = request.form["year"]
    if year != "":
        rawData = requests.get(
            "http://www.omdbapi.com/?apikey=" + apiKey + "&t="+title+"&y="+year)
    else:
        rawData = requests.get(
            "http://www.omdbapi.com/?apikey=" + apiKey + "&t="+title)
    movie = rawData.json()
    return render_template("search.html", movie=movie)


@app.route("/favorite_list")
def favorite_list():
    favorite_list = session.get("favorite")
    if favorite_list == None:
        flash("Your favorite list is empty")
        return redirect(url_for("main"))
    else:
        return render_template("favorite.html", favorite_list=favorite_list)


@app.route("/add_to_favorite/<title>")
def add_to_favorite(title):
    favorite_list = {}
    if "favorite" in session:
        favorite_list = session.get("favorite")
    else:
        session["favorite"] = {}
    favorite_list[title] = title
    session["favorite"] = favorite_list
    return redirect(url_for("main"))


@app.route("/remove_from_list/<title>")
def remove_from_list(title):
    favorite_list = session.get("favorite")
    favorite_list.pop(title, None)
    session["favorite"] = favorite_list
    return redirect(url_for("favorite_list"))


if __name__ == "__main__":
    app.run(debug=True)

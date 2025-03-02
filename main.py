from flask import Flask, render_template, request
import sqlite3

app: Flask = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index() -> str:
    db = sqlite3.connect("db/database.db")
    countries = tuple(db.execute("select name from countries order by id asc"))
    db.close()

    countries = [country[0] for country in countries]

    if request.method == "GET":
        return render_template("index.html", countries=countries)

    if request.method == "POST":
        country = request.form["Country"]

        if country == "Select country":
            return render_template("index.html", countries=countries)

        arcades = ["Virtualand", "Timezone"]
        return render_template("index.html", countries=countries, arcades=arcades)


if __name__ == "__main__":
    app.run(debug=True, port=6942)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app: Flask = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index() -> str:
    db = sqlite3.connect("db/database.db")
    countries = tuple(
        db.execute("select name, country_code from countries order by id asc")
    )
    db.close()

    country_data = dict([(country[0], country[1]) for country in countries])

    if request.method == "GET":
        return render_template(
            "index.html", countries=[country for country in country_data.keys()]
        )

    if request.method == "POST":
        selected_country = request.form["Country"]

        if selected_country not in country_data.keys():
            pass

        if selected_country == "Select country":
            render_template(
                "index.html",
                countries=[country for country in country_data.keys()],
                selected_country="",
            )

        return redirect(url_for(f"country", selected_country=selected_country))


@app.route("/<selected_country>/")
def country(selected_country: str):
    return render_template("country.html", selected_country=selected_country)


if __name__ == "__main__":
    app.run(debug=True, port=6942)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app: Flask = Flask(__name__)


# In case database name changes
def connect() -> sqlite3.Connection:
    return sqlite3.connect("db/database.db")


@app.route("/", methods=["POST", "GET"])
def index() -> str:
    country_data = None

    with connect() as db:
        countries = tuple(db.execute("select name from countries order by id asc"))

        country_data = [country[0] for country in countries]

    countries = [country for country in country_data]

    if request.method == "GET":
        return render_template("index.html", countries=countries)

    if request.method == "POST":
        selected_country = request.form["Country"]

        if selected_country not in country_data:
            pass

        if selected_country == "Select country":
            render_template("index.html", countries=countries)

        return redirect(url_for(f"country", selected_country=selected_country))


@app.route("/<selected_country>/")
def country(selected_country: str):
    arcades = None
    with connect() as db:
        arcades = [
            arcade[0]
            for arcade in db.execute(
                """ select arcades.name from arcades 
                    join countries on arcades.country_id = countries.id 
                    where countries.name = ?""",
                (selected_country,),
            )
        ]

    return render_template(
        "country.html", selected_country=selected_country, arcades=arcades
    )


@app.route("/<selected_country>/<arcade>/")
def arcade(selected_country: str, arcade: str):
    cabinets = None
    arcade_info = None
    with connect() as db:
        cabinets = db.execute(
            """ select cabinets.cabinet_name,  cabinet_info.cost_per_game, cabinet_info.count from cabinets 
                join cabinet_info on cabinet_info.cabinet_id = cabinets.cabinet_id 
                join arcades on cabinet_info.arcade_id = arcades.arcade_id
                where arcades.name = ?;""",
            (arcade,),
        )

        arcade_info = db.execute(
            """ select arcades.address, arcades.phone_no, arcades.operating_time, arcades.website from arcades
                where arcades.name = ?;""",
            (arcade,),
        )

    cabinets = [
        (cabinet[0].strip(), cabinet[1].strip(), cabinet[2]) for cabinet in cabinets
    ]
    # If there's more than 1, I think we're really fucked now
    arcade_info = list(arcade_info)[0]

    address = arcade_info[0].strip()
    phone_no = arcade_info[1]
    operating_time = arcade_info[2]
    website = arcade_info[3]

    print(address)

    return render_template(
        "arcade.html",
        arcade=arcade,
        address=address,
        phone_no=phone_no,
        operating_time=operating_time,
        website=website,
        cabinets=cabinets,
    )


if __name__ == "__main__":
    app.run(debug=True, port=6942)

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

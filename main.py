from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
import sqlite3, os
from waitress import serve

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

        if selected_country == "Select country":
            return render_template("index.html", countries=countries)

        return redirect(url_for(f"country", selected_country=selected_country))


@app.route("/<selected_country>/")
def country(selected_country: str):

    arcades = None
    with connect() as db:
        country = list(
            db.execute(
                """ select countries.name from countries 
                    where countries.name like ?""",
                (selected_country,),
            )
        )

        if country == []:
            return render_template("elements/404.html", unfound=selected_country)

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
            """ select arcades.address, arcades.phone_no, arcades.operating_time, arcades.website, arcades.completed, arcades.last_updated from arcades
                where arcades.name = ?;""",
            (arcade,),
        )

    cabinets: list[tuple] = [
        (cabinet[0].strip(), cabinet[1].strip(), cabinet[2]) for cabinet in cabinets
    ]

    # If there's more than 1, I think we're really fucked now
    arcade_info = list(arcade_info)[0]

    address: str = arcade_info[0].strip()
    phone_no: str = arcade_info[1]
    operating_time: str = arcade_info[2]
    website: str = arcade_info[3]
    completed: bool = bool(arcade_info[4])
    last_updated: str = arcade_info[5]

    return render_template(
        "arcade.html",
        arcade=arcade,
        address=address,
        phone_no=phone_no,
        operating_time=operating_time,
        website=website,
        cabinets=cabinets,
        completed=completed,
        last_updated=last_updated,
    )


@app.route("/favicon.ico/")
def favicon():
    # return send_from_directory(
    #     os.path.join(app.root_path, "static"),
    #     "favicon.ico",
    #     mimetype="image/vnd.microsoft.icon",
    # )
    return ("", 204)


@app.route("/cabinets/<cabinet>/")
def cabinets(cabinet: str) -> str:
    cabinet_name = None
    cabinet_desc = None

    print(f"'{cabinet}'")
    with connect() as db:
        cabinet_data = list(
            db.execute(
                """ select cabinet_name, cabinet_description from cabinets 
                where cabinet_name like ?;""",
                (cabinet,),
            )
        )

        if cabinet_data == []:
            return render_template("elements/404.html", unfound=cabinet)

        cabinet_name = cabinet_data[0][0]
        cabinet_desc = cabinet_data[0][1].split("\n")

    return render_template(
        "cabinets.html", cabinet_name=cabinet_name, cabinet_desc=cabinet_desc
    )


@app.route("/cabinets/")
def cabinet_list() -> str:
    cabinet_list = None

    with connect() as db:
        cabinet_data = list(db.execute(""" select cabinet_name from cabinets; """))
        cabinet_list = [cabinet[0] for cabinet in cabinet_data]

    return render_template("cabinet_list.html", cabinet_list=cabinet_list)


@app.route("/404/")
def not_found() -> str:
    return render_template("elements/404.html")


@app.route("/404/<unfound>/")
def not_found_url(unfound: str) -> str:
    return render_template("elements/404.html", unfound=unfound)


if __name__ == "__main__":
    # app.run(debug=True, port=6942)

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    serve(app, host="127.0.0.1", port=6942, expose_tracebacks=True, threads=5)

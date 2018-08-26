from app import app_inst
from Classes import *
from flask import request, render_template, url_for
import pickle
from werkzeug.utils import redirect


@app_inst.route("/")
@app_inst.route("/index")
def index():
    with open(file_name, "rb") as file:
        week = pickle.load(file)
    return render_template("index.html", title="home", week=week)


@app_inst.route("/add_chore", methods=["GET", "POST"])
def add_chore():
    day = int(request.form["day"])
    chore = request.form["chore"]
    assigned_to = request.form["name"]
    color = request.form["color"]
    new_chore = Chore(chore, User(assigned_to, color))
    with open(file_name, "rb") as file:
        week = pickle.load(file)
        week.add_chore(new_chore, day)
    with open(file_name, "wb") as file:
        pickle.dump(week, file)

    return redirect(url_for("index"))


from app import app_inst
from Classes import Chore, User, Day, Week
from flask import render_template
import pickle
from datetime import date


file_name = "storage"


@app_inst.route("/")
@app_inst.route("/index")
def index():
    with open(file_name, "rb") as file:
        week = pickle.load(file)
    return render_template("index.html", title="home", week=week)

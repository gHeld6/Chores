from app import app_inst
from Classes import *
from flask import render_template
import pickle


@app_inst.route("/")
@app_inst.route("/index")
def index():
    with open(file_name, "rb") as file:
        week = pickle.load(file)
    return render_template("index.html", title="home", week=week)

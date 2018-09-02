from app import app_inst, db
from Classes import *
from app.models import *
from flask import request, render_template, url_for, flash
import pickle
from werkzeug.utils import redirect
from app.forms import AddChoreForm


@app_inst.route("/", methods=["GET", "POST"])
@app_inst.route("/index", methods=["GET", "POST"])
def index():
    with open(file_name, "rb") as file:
        week = pickle.load(file)
    form = AddChoreForm()
    users = User.query.all()
    for u in users:
        flash(u)
    return render_template("index.html", title="home", week=week, form=form, users=users)


@app_inst.route("/delete_chore", methods=["GET", "POST"])
def delete_chore():
    return redirect("/index")


@app_inst.route("/add_chore", methods=["GET", "POST"])
def add_chore():
    form = AddChoreForm()
    if form.validate_on_submit():
        day = form.day.data
        chore = form.new_chore.data
        user = form.user.data
        add_chore_list(day, chore, user)
        print("day: {d}, chore: {c}, user: {u}".format(d=str(day), c=chore, u=user))
    return redirect("/index")
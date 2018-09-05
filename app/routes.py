from app import app_inst, db
from Classes import *
from app.models import *
from flask import request, render_template, url_for, flash, redirect
import pickle
from app.forms import AddChoreForm


@app_inst.route("/", methods=["GET", "POST"])
@app_inst.route("/index", methods=["GET", "POST"])
def index():
    with open(file_name, "rb") as file:
        week = pickle.load(file)
    form = AddChoreForm()
    days = [[],[],[],[],[],[],[]]
    chores = Chore.query.order_by(Chore.day).all()
    for chore in chores:
        days[chore.day].append((chore.chore, User.query.filter_by(id=chore.user_id).first().name, chore.id))
    users = User.query.all()
    for c in chores:
        flash(c)
    for u in users:
        flash(u)
    return render_template("index.html", title="home", week=week, form=form, chores=chores, days=days, day_names=DAY_NAMES)


@app_inst.route("/delete_chore", methods=["GET", "POST"])
def delete_chore():
    return redirect("/index")


@app_inst.route("/add_chore", methods=["GET", "POST"])
def add_chore():
    form = AddChoreForm()
    day_field = form.day.data
    chore_field = form.new_chore.data
    user_field = form.user.data
    u = User.query.filter_by(name=user_field).first()
    c = Chore(chore=chore_field, day=int(day_field), user=u)
    db.session.add(c)
    db.session.commit()
    return redirect("/index")

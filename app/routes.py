from app import app_inst, db
from Classes import *
from app.models import *
from flask import request, render_template, flash, redirect
from app.forms import AddChoreForm


@app_inst.route("/", methods=["GET", "POST"])
@app_inst.route("/index", methods=["GET", "POST"])
def index():
    form = AddChoreForm()
    days = get_days()
    users = User.query.all()
    return render_template("index.html", title="home", form=form, days=days, day_names=DAY_NAMES)


@app_inst.route("/delete_chore", methods=["GET", "POST"])
def delete_chore():
    n_id = request.args.get("id")
    c = Chore.query.filter_by(id=n_id).first()
    db.session.delete(c)
    db.session.commit()
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

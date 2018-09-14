from app import app_inst, db
from header import *
from app.models import *
from flask import request, render_template, flash, redirect, jsonify
from app.forms import AddChoreForm
from datetime import date


@app_inst.route("/", methods=["GET", "POST"])
@app_inst.route("/index", methods=["GET", "POST"])
def index():
    form = AddChoreForm()
    days = get_days()
    cur_day = date.today().weekday()
    return render_template("index.html", title="home", form=form, days=days, day_names=DAY_NAMES, cur_day=int(cur_day))


@app_inst.route("/delete_chore", methods=["GET", "POST"])
def delete_chore():
    n_id = request.args.get("id")
    c = Chore.query.filter_by(id=n_id).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/index")


@app_inst.route("/add_chore_ajax", methods=["POST"])
def add_chore_ajax():
    form = AddChoreForm()
    day = form.day.data
    chore = form.new_chore.data
    user = form.user.data
    u = User.query.filter_by(name=user).first()
    c = Chore(chore=chore, day=int(day), user=u)
    db.session.add(c)
    db.session.commit()
    return jsonify(data={'day': DAY_NAMES[int(day)], 'chore': chore, 'user': user, 'id': c.id})


@app_inst.route("/del_chore_ajax", methods=["POST"])
def del_chore_ajax():
    c_id = int(request.form["id"])
    chore = Chore.query.filter_by(id=c_id).first()
    if not chore:
        flash("Chore not found for id:{}".format(c_id))
        return redirect("/index")
    db.session.delete(chore)
    db.session.commit()
    return jsonify(data={'id': c_id})
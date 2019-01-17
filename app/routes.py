from app import app_inst, db
from header import *
from app.models import Chore, User
from flask import request, render_template, flash, redirect, jsonify
from app.forms import AddChoreForm
import datetime


@app_inst.route("/", methods=["GET", "POST"])
@app_inst.route("/index", methods=["GET", "POST"])
def index():
    form = AddChoreForm()
    form.user.choices = [(u.name, u.name) for u in User.query.all()]
    days = get_days()
    cur_day = date.today().weekday()
    return render_template("index.html", title="home", form=form, days=days,
                           day_names=DAY_NAMES, cur_day=int(cur_day), times=TIMES)


@app_inst.route("/delete_chore", methods=["GET", "POST"])
def delete_chore():
    n_id = request.args.get("id")
    c = Chore.query.filter_by(id=n_id).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/index")


@app_inst.route("/add_chore_ajax", methods=["POST"])
def add_chore_ajax():
    tf = int(request.form["time_field"])
    if request.form.get("notify") != "Yes":
        tf = 24
    rec = request.form.get("recurring")
    form = AddChoreForm()
    chore = form.new_chore.data
    if chore == "":
        flash("Chore field must not be empty")
        return render_template("index.html", title="home", form=form,
                               days=get_days(), day_names=DAY_NAMES,
                               cur_day=int(date.today().weekday()), times=TIMES)
    day = form.day.data
    user = form.user.data
    u = User.query.filter_by(name=user).first()
    c = Chore(chore=chore, day=int(day), user=u, time_completed_by=tf, recurring=(rec == "Yes"))
    db.session.add(c)
    db.session.commit()
    if rec != "Yes":
        rec = "No"
    return jsonify(data={'day': DAY_NAMES[int(day)], 'chore': chore, 'user': user,
                         'id': c.id, 'time': TIMES[tf - 1][1], "recurring": rec})


@app_inst.route("/del_chore_ajax", methods=["POST"])
def del_chore_ajax():
    c_id = int(request.form["id"])
    day = request.form["day"]
    chore = Chore.query.filter_by(id=c_id).first()
    if not chore:
        flash("Chore not found for id:{}".format(c_id))
        return redirect("/index")
    db.session.delete(chore)
    db.session.commit()
    return jsonify(data={'id': c_id, 'day': day})


@app_inst.route("/edit_users", methods=["GET"])
def edit_users():
    users = get_users()
    return render_template("updateUser.html", colors=list(rgb_vals.keys()), users=users)


@app_inst.route("/change_user_info", methods=["POST"])
def change_user_info():
    u_id = request.form["id"]
    u = User.query.filter_by(id=int(u_id)).first()
    u.name = request.form["name"]
    u.color = request.form["color"]
    u.token = request.form["tok"]
    db.session.commit()
    flash("Update successful")
    return redirect("/edit_users")

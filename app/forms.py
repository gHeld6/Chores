from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import *


class AddChoreForm(FlaskForm):
    users = User.query.all()
    length = len(users)
    while length < 2:
        u = User(name="User{}".format(len))

    user = SelectField("User", choices=[(users[0].name, users[0].name), (users[1].name, users[1].name)])
    new_chore = StringField("Chore", validators=[DataRequired()])
    day = SelectField("Day", choices=[(0,"Monday"), (1, "Tuesday"), (2, "Wednesday") , (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")])
    submit = SubmitField("Add Chore")
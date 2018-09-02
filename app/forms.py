from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from Classes import file_name, get_week
from app.models import *


class AddChoreForm(FlaskForm):
    week = get_week()
    users = User.query.all()
    user = SelectField("User", choices=[(users[0].name, users[0].name), (users[1].name, users[1].name)])
    new_chore = StringField("Chore", validators=[DataRequired()])
    day = SelectField("Day", choices=[(1,"Monday"), (2, "Tuesday"), (3, "Wednesday") , (4, "Thursday"), (5, "Friday"), (6, "Saturday"), (7, "Sunday")])
    submit = SubmitField("Add Chore")
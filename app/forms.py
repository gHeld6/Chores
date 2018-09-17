from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import *


class AddChoreForm(FlaskForm):
    user = SelectField("User", choices=[])
    new_chore = StringField("Chore", validators=[DataRequired()])
    day = SelectField("Day", choices=[(0,"Monday"), (1, "Tuesday"), (2, "Wednesday") , (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")])
    submit = SubmitField("Add Chore")


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.validators import Required
from wtforms_components import TimeField
from header import TIMES
import datetime

class AddChoreForm(FlaskForm):
    
    user = SelectField("User", choices=[])
    new_chore = StringField("Chore", validators=[Required("Please enter a chore")])
    day = SelectField("Day", choices=[(0,"Monday"), (1, "Tuesday"), (2, "Wednesday") , (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")])
    time_field = SelectField("Notification Time", choices=TIMES)
    recurring = RadioField("Recurring", choices=[("True", True),
                                                 ("False", False)])
    submit = SubmitField("Add Chore")
    
    

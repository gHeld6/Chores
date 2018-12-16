from app import db
import datetime


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    chore = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    completed = db.Column(db.Boolean, default=False)
    time_completed_by = db.Column(db.DateTime)
    
    def __repr__(self):
        return "<Chore {}>".format(self.chore)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    led = db.Column(db.Integer)
    name = db.Column(db.String(40), index=True, unique=True)
    color = db.Column(db.String(20), index=True)
    numChores = db.Column(db.Integer, default=0)
    chores = db.relationship("Chore", backref="user")

    def __repr__(self):
        return "<User: name:{}>".format(self.name)

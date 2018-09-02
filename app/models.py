from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    color = db.Column(db.String(20), index=True)
    numChores = db.Column(db.Integer, default=0)
    c_list = db.relationship("Chore", backref="assignedTo", lazy="dynamic")

    def __repr__(self):
        return "User: {name}, Color: {color}".format(name=self.name, color=self.color)


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    chore = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "Chore: {}".format(self.chore)

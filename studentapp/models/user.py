from studentapp.models import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255))
	name = db.Column(db.String(255))
	dt = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, index = True)
	username = db.Column(db.String(64), index=True)
	num1 = db.Column(db.Integer)
	prog = db.Column(db.Integer)
	n_attempts = db.Column(db.Integer)

def __init__(self, email, name, dt, user_id, username, num1, prog, one_attempt, multiple_attempts, not_completed):
	self.email = email
	self.name = name
	self.dt = dt
	self.user_id = user_id
	self.username = username
	self.num1 = num1
	self.nproblems_attempted = nproblems_attempted
	self.n_attempts = n_attempts


def __repr__(self):
	return '<User %r>' % (self.username)




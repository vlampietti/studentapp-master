from studentapp.models import db
from datetime import datetime

class UserData(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	user_id = db.Column(db.Integer, index = True)
	username = db.Column(db.String(64), index=True)
	login_date = db.Column(db.DateTime)
	ndays_act = db.Column(db.Integer)
	nproblems_attempted = db.Column(db.Integer)
	one_attempt = db.Column(db.Integer)
	multiple_attempts = db.Column(db.Integer)
	not_completed = db.Column(db.Integer)
	months = db.Column(db.String(64))
	

def __init__(self, user_id, username, login_date, ndays_act, nproblems_attempted, one_attempt, multiple_attempts, not_completed, months):
	self.user_id = user_id
	self.username = username
	self.login_date = login_date
	self.ndays_act = ndays_act
	self.nproblems_attempted = nproblems_attempted
	self.one_attempt = one_attempt
	self.multiple_attempts = multiple_attempts
	self.not_completed = not_completed
	self.months = months

def __repr__(self):
	return '<UserData %r>' % (self.username)

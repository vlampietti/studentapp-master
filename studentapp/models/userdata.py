from studentapp.models import db
from datetime import datetime

class UserData(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	user_id = db.Column(db.Integer, index = True, unique=True)
	username = db.Column(db.String(64), index=True, unique=True)
	query_date = db.Column(db.String(64))
	ndays_act = db.Column(db.Integer)
	completed = db.Column(db.Integer)
	not_completed = db.Column(db.Integer)
	one_attempt = db.Column(db.Integer)
	multiple_attempts = db.Column(db.Integer)
	

def __init__(self, user_id, username, query_date, ndays_act, completed, not_completed, one_attempt, multiple_attempts):
	self.user_id = user_id
	self.username = username
	self.query_date = query_date
	self.ndays_act = ndays_act
	self.completed = completed
	self.not_completed = not_completed
	self.one_attempt = one_attempt
	self.multiple_attempts = multiple_attempts

def __repr__(self):
	return '<UserData %r>' % (self.username)


from studentapp.models import db
from datetime import datetime

class UserActivity(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	user_id = db.Column(db.Integer, index = True, unique=True)
	username = db.Column(db.String(64), index=True, unique=True)
	query_date = db.Column(db.String(64))
	daily_activity = db.Column(db.String)
	

def __init__(self, user_id, username, query_date, daily_activity):
	self.user_id = user_id
	self.username = username
	self.query_date = query_date
	self.daily_activity = daily_activity

def __repr__(self):
	return '<UserActivity %r>' % (self.username)


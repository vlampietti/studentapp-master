from studentapp.models import db
from datetime import datetime

class ButtonClicks(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	user_id = db.Column(db.Integer, index = True)
	username = db.Column(db.String(64), index=True)
	login_date = db.Column(db.DateTime)
	nforum_click = db.Column(db.Integer)

def __init__(self, user_id, username, login_date, nforum_click):
	self.user_id = user_id
	self.username = username
	self.login_date = login_date
	self.nforum_click = nforum_click

def __repr__(self):
	return '<ButtonClicks %r>' % (self.username)
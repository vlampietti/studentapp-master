from studentapp.models import db
from datetime import datetime

class UserLogin(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	user_id = db.Column(db.Integer, index = True)
	username = db.Column(db.String(64), index=True)
	login_date = db.Column(db.DateTime)
	device = db.Column(db.String(64))
	nforum_click = db.Column(db.Integer)
	ip_address = db.Column(db.String(64))

def __init__(self, user_id, username, login_date, device, nforum_click, ip_address):
	self.user_id = user_id
	self.username = username
	self.login_date = login_date
	self.device = device
	self.nforum_click = nforum_click
	self.ip_address = ip_address

def __repr__(self):
	return '<UserLogin %r>' % (self.username)
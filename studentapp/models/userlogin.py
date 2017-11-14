from studentapp.models import db
from datetime import datetime

class UserLogin(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	user_id = db.Column(db.Integer, index = True)
	username = db.Column(db.String(64), index=True)
	login_date = db.Column(db.DateTime)
	ip_address = db.Column(db.String(64))
	device = db.Column(db.String(64))
	browser = db.Column(db.String(64))
	

def __init__(self, user_id, username, login_date, ip_address, device, browser):
	self.user_id = user_id
	self.username = username
	self.login_date = login_date
	self.ip_address = ip_address
	self.device = device
	self.browser = browser

def __repr__(self):
	return '<UserLogin %r>' % (self.username)
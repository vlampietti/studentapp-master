from flask import Flask


app = Flask(__name__)


import os
app.config.from_object('config')

import studentapp.controllers

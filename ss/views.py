import json

from flask import Blueprint, render_template

from ss.models import Logins

views = Blueprint('views', __name__, template_folder="templates/ss")


# @views.route('/')
# def index():
#     login = Logins()
#     arian = login.get()
#     return render_template('index.html')

import json

from flask import Blueprint, render_template, jsonify

from ss.models import Logins

views = Blueprint('views', __name__, template_folder="templates/ss")


@views.route('/')
def index():
    login = Logins('http://127.0.0.1:8000')
    arian = login.get()
    return json.dumps(arian.json())

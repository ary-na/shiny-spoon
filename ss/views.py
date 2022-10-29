from flask import Blueprint, render_template

from ss.models import login_required

views = Blueprint('views', __name__, template_folder="templates/ss")


@views.route('/')
@login_required
def index():
    return render_template('index.html')

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home_new():
    return render_template("home_new.html", user=current_user)


# @views.route('/home-guest', methods=['GET', 'POST'])
# def home_guest():
#     return render_template("home_new.html")


@views.route('/home-loged-in', methods=['GET', 'POST'])
@login_required
def home_loged_in():
    return render_template("home_loged_in.html", user=current_user)



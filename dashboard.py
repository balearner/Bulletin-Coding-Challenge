from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import pandas as pd
from . import housing_db
import json

dashboard = Blueprint('dashboard', __name__)
housing_collection = housing_db.listingsAndReviews


# return all the result in the dataset and present them in a form of database
@dashboard.route('/dashboard', methods=['GET', 'POST', 'OPTIONS'])
@login_required
def show_dashboard(page=1, **kargs):
    page = request.args.get('page', 1, type=int)
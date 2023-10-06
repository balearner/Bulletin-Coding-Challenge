from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import pandas as pd
from . import housing_db
import json

query = Blueprint('query', __name__)
housing_collection = housing_db.listingsAndReviews


# return all the result in the dataset and present them in a form of database
@query.route('/result-all', methods=['GET', 'POST', 'OPTIONS'])
@login_required
def result_all(page=1, **kargs):
    page = request.args.get('page', 1, type=int)

    # Calculate the number of items to skip to fetch the desired page
    items_per_page = 20
    skip = (page - 1) * items_per_page

    filter_criteria = {}
    if request.method == 'GET':
        # Get filter criteria from the submitted form
        property_type = request.args.get('property_type')
        accommodates = request.args.get('accommodates')
        bedrooms = request.args.get('bedrooms')
        bathrooms = request.args.get('bathrooms')

        # Build filter criteria based on user selections
        if property_type:
            filter_criteria['property_type'] = property_type

        if accommodates:
            if accommodates == '5+':
                filter_criteria['accommodates'] = {"$gt": 5}
            else:
                filter_criteria['accommodates'] = int(accommodates)

        if bedrooms:
            if bedrooms == '4+':
                filter_criteria['bedrooms'] = {"$gt": 4}
            else:
                filter_criteria['bedrooms'] = int(bedrooms)

        if bathrooms:
            if bathrooms == '3+':
                filter_criteria['bathrooms'] = {"$gt": 3}
            else:
                filter_criteria['bathrooms'] = int(bathrooms)

    if filter_criteria:
        result = housing_collection.find(filter_criteria).skip(skip).limit(items_per_page)
    else:
        result = housing_collection.find().skip(skip).limit(items_per_page)

    # Calculate the Number of Pages
    total_items = housing_collection.count_documents({})
    num_pages = (total_items + items_per_page - 1) // items_per_page  # Calculate total pages

    # Select the desired fields from the MongoDB documents
    selected_fields = ['name', 'summary', 'property_type', 'accommodates', 'bedrooms', 'bathrooms']
    selected_data = []

    for item in result:
        selected_item = {field: item.get(field, None) for field in selected_fields}
        selected_data.append(selected_item)

    df = pd.DataFrame(selected_data)
    if filter_criteria:
        return render_template('filter_result.html', data=df, user=current_user, num_pages=num_pages, page=page,property_type=property_type,
        accommodates=accommodates,
        bedrooms=bedrooms,
        bathrooms=bathrooms)
    else:
        return render_template('result.html', data=df, user=current_user, num_pages=num_pages, page=page,property_type=property_type,
        accommodates=accommodates,
        bedrooms=bedrooms,
        bathrooms=bathrooms)





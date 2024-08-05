#!/usr/bin/python3
"""routes for the Flask API"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def app_status():
    """ get status and return a json respons"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """
    get_stats is an endpoint that retrieves
    the number of each objects by type
    """
    class_models = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
    }
    all_stats = {}

    for m_name, m_class in class_models.items():
        all_stats[m_name] = storage.count(class_models)

    return jsonify(all_stats)

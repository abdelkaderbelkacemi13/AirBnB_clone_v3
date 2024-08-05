#!/usr/bin/python3
"""routes for the Flask API"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def app_status():
    """ get status and return a json respons"""
    return jsonify({"status": "OK"})

#!/usr/bin/python3
""" handel the Bleuprint for the flask
        application
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.states import *

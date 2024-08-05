#!/usr/bin/python3
"""The flask application API """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
apphost = os.getenv('HBNB_API_HOST', '0.0.0.0')
appport = os.getenv('HBNB_API_PORT', '5000')
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """Method to handel @app.teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def not_found_404(error):
    """This is a handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=apphost,
        port=int(appport),
        threaded=True
    )

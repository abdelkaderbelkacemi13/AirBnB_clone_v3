#!/usr/bin/python3
"""The flask application API """

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """Method to handel @app.teardown_appcontext"""
    storage.close()


if __name__ == "__main__":
    apphost = os.getenv('HBNB_API_HOST', '0.0.0.0')
    appport = os.getenv('HBNB_API_PORT', '5000')
    app.run(
        host=apphost,
        port=appport,
        threaded=True
    )

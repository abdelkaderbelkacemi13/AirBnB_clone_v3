#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions:
"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get all states"""
    states = storage.all(States)
    return (jsonify(list(map(lambda s: s.to_dict(), states.values()))))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get individual state based on id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """to update state based on passed http body req"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    keys_to_ignore = ['id', 'created_at', 'updated_at']
    update_data = request.get_json()

    if not update_data:
        abort(400, description="Not a JSON")

    for key, value in update_data:
        if key not in keys_to_ignore:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """to create a new state based on passed http body req"""
    if not request.json:
        abort(400, description='Not a JSON')
    if 'name' not in request.json:
        abort(400, description='Missing name')

    state_data = request.get_json()
    state = State(**state_data)
    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete state based on id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify(state.to_dict()), 200)

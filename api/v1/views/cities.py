#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions:
"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """method to retrieve all States"""
    states = storage.all(State).values()
    return (jsonify(list(map(lambda state: state.to_dict(), states))))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """create a state"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing Name")

    data = request.get_json()
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates state """
    state = storage.get(State, state_id)
    if not state:
        abort(400)
    if not request.json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'updated_at', 'created_at']
    for key, value in data:
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes state"""
    state = (storage.get(State, state_id))
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

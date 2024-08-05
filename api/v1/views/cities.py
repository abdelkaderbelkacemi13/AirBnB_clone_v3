#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions:
"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """method to retrieve all cities in a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return (jsonify(list(map(lambda city: city.to_dict(), states.cities))))


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return (jsonify(city.to_dict()))


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_state(state_id):
    """create a city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)
